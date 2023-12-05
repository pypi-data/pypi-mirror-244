import numpy as np
import pandas as pd

from skimage import measure
from skimage import morphology

from cryocat import cryomap
from cryocat import geom
from cryocat import visplot
from cryocat import cryomotl
from cryocat import cryomask

from lmfit import models
import skimage


def compute_scores_map_threshold_triangle(scores_map):
    sp = np.sort(scores_map, axis=None)
    nbins = len(sp)

    # Find peak, lowest and highest gray levels.
    arg_peak_height = np.argmax(sp)
    peak_height = sp[arg_peak_height]
    arg_low_level, arg_high_level = np.where(sp > 0)[0][[0, -1]]

    # Flip is True if left tail is shorter.
    flip = arg_peak_height - arg_low_level < arg_high_level - arg_peak_height
    if flip:
        sp = sp[::-1]
        arg_low_level = nbins - arg_high_level - 1
        arg_peak_height = nbins - arg_peak_height - 1

    # If flip == True, arg_high_level becomes incorrect
    # but we don't need it anymore.
    del arg_high_level

    # Set up the coordinate system.
    width = arg_peak_height - arg_low_level
    x1 = np.arange(width)
    y1 = sp[x1 + arg_low_level]

    # Normalize.
    norm = np.sqrt(peak_height**2 + width**2)
    peak_height /= norm
    width /= norm

    # Maximize the length.
    # The ImageJ implementation includes an additional constant when calculating
    # the length, but here we omit it as it does not affect the location of the
    # minimum.
    length = peak_height * x1 - width * y1
    arg_level = np.argmax(length) + arg_low_level

    if flip:
        arg_level = nbins - arg_level - 1

    return sp[arg_level]


def create_starting_parameters_1D(input_map, peak_tolerance=20):
    peak_mask = cryomask.spherical_mask(np.asarray(input_map.shape), radius=peak_tolerance)
    masked_map = input_map * peak_mask
    peak_center = np.unravel_index(np.argmax(masked_map), shape=masked_map.shape)
    peak_height = np.amax(input_map)

    x_profile = input_map[:, peak_center[1], peak_center[2]]
    y_profile = input_map[peak_center[0], :, peak_center[2]]
    z_profile = input_map[peak_center[0], peak_center[1], :]

    profiles = np.vstack((x_profile, y_profile, z_profile))

    return peak_center, peak_height, profiles.T


def create_starting_parameters_2D(input_map, peak_tolerance=20, peak_center=None):
    peak_mask = cryomask.spherical_mask(np.asarray(input_map.shape), radius=peak_tolerance)
    masked_map = input_map * peak_mask
    if peak_center is None:
        peak_center = np.unravel_index(np.argmax(masked_map), shape=masked_map.shape)
        peak_height = np.amax(input_map)
    else:
        peak_height = masked_map[peak_center[0], peak_center[1], peak_center[2]]

    xy_plane = input_map[:, :, peak_center[2]]
    yz_plane = input_map[peak_center[0], :, :]
    xz_plane = input_map[:, peak_center[1], :]

    slices = np.stack((xy_plane, yz_plane, xz_plane), axis=2)

    return peak_center, peak_height, slices


def compute_gaussian_threshold(input_map):
    pc, ph, profiles = create_starting_parameters_1D(input_map, peak_tolerance=20)

    heights = []
    for i in range(3):
        rt_line = profiles[:, i]
        x = np.linspace(0, rt_line.shape[0], rt_line.shape[0])
        y = rt_line
        mod = models.GaussianModel()

        # params = mod.make_params(center=24, sigma=0.5)
        params = mod.guess(rt_line, x)

        # you can place min/max bounds on parameters
        params["amplitude"].min = 0
        params["sigma"].min = 0
        params["center"].min = pc[i] - 1
        params["center"].max = pc[i] + 1

        # pars = mod.guess(y, x=x)
        out = mod.fit(y, params, x=x)

        heights.append(out.params["height"].value)

    return np.mean(np.asarray(heights))


def get_ellipsoid_label(input_map, peak_coordinates, map_threshold=0.0):
    th_map = np.where(input_map == map_threshold, 2.0, 1.0)  # shift the thresholding, otherwise only 1 label is found
    labeled_th_map = measure.label(th_map, connectivity=1)
    central_label = labeled_th_map[peak_coordinates[0], peak_coordinates[1], peak_coordinates[2]]
    th_map = np.where(labeled_th_map == central_label, 1.0, 0.0)

    ellipsoid_verts, _, _, _ = measure.marching_cubes(th_map, level=0.5)
    idx = np.round(ellipsoid_verts).astype(int)
    surface_fit = np.zeros(th_map.shape)
    surface_fit[idx[:, 0], idx[:, 1], idx[:, 2]] = 1.0

    _, radii, radii_dir, ell_params = geom.fit_ellipsoid(ellipsoid_verts)

    # dist = np.zeros(3,)
    # for i in range(3):
    #    dist[i] = np.linalg.norm(ellipsoid_verts[ellipsoid_verts[:, i].argsort()][-1,:] - ellipsoid_verts[ellipsoid_verts[:, i].argsort()][0,:], axis=0)

    # sorted_idx = np.argsort(dist)
    # radii_sorted = radii[sorted_idx]

    sorted_idx = np.argmax(np.abs(radii_dir), axis=0)
    radii_sorted = radii[sorted_idx] * 2.0

    fitted_label = geom.fill_ellipsoid(th_map.shape, ell_params)

    return fitted_label, radii_sorted, surface_fit, th_map


def get_central_plane_labels(input_map, peak_coordinates, map_threshold=0.0):
    th_map = np.where(input_map == map_threshold, 2.0, 1.0)  # shift the thresholding, otherwise only 1 label is found
    # labeled_th_map = measure.label(th_map, connectivity = 1)
    # central_label = labeled_th_map[peak_coordinates[0],peak_coordinates[1],peak_coordinates[2]]
    # th_map = np.where(labeled_th_map == central_label, 2.0, 1.0)

    planes = np.zeros((input_map.shape[0], input_map.shape[1], 3))  # works only for cubic volumes!!!
    planes[:, :, 0] = th_map[:, :, peak_coordinates[2]]
    planes[:, :, 1] = th_map[peak_coordinates[0], :, :]
    planes[:, :, 2] = th_map[:, peak_coordinates[1], :]

    label_mask = np.zeros(input_map.shape)
    ellipse_masks = np.zeros(planes.shape)
    size_x, size_y, size_z = (0.0, 0.0, 0.0)

    for i in range(3):
        plane_label = measure.label(planes[:, :, i], connectivity=1)
        plane_props = pd.DataFrame(
            measure.regionprops_table(
                plane_label, properties=["label", "centroid", "axis_major_length", "axis_minor_length", "orientation"]
            )
        )

        if i < 2:
            central_label = plane_label[peak_coordinates[i], peak_coordinates[i + 1]]
        else:
            central_label = plane_label[peak_coordinates[0], peak_coordinates[i]]

        plane_props = plane_props[plane_props["label"] == central_label].reset_index()

        ellipse_indices = skimage.draw.ellipse(
            plane_props.at[0, "centroid-0"],
            plane_props.at[0, "centroid-1"],
            plane_props.at[0, "axis_major_length"] * 0.5,
            plane_props.at[0, "axis_minor_length"] * 0.5,
            rotation=plane_props.at[0, "orientation"],
        )
        ellipse_indices_x = np.clip(ellipse_indices[0], 0, input_map.shape[0] - 1)
        ellipse_indices_y = np.clip(ellipse_indices[1], 0, input_map.shape[1] - 1)

        if plane_props.at[0, "orientation"] < 0.0:
            major_axis = plane_props.at[0, "axis_major_length"]
            minor_axis = plane_props.at[0, "axis_minor_length"]
        else:
            major_axis = plane_props.at[0, "axis_minor_length"]
            minor_axis = plane_props.at[0, "axis_major_length"]

        ellipse_masks[ellipse_indices_x, ellipse_indices_y, i] = 1.0

        if i == 0:
            size_x += minor_axis
            size_y += major_axis
        elif i == 1:
            size_y += minor_axis
            size_z += major_axis
        else:
            size_x += minor_axis
            size_z += major_axis

    label_mask[:, :, peak_coordinates[2]] += ellipse_masks[:, :, 0]
    label_mask[peak_coordinates[0], :, :] += ellipse_masks[:, :, 1]
    label_mask[:, peak_coordinates[1], :] += ellipse_masks[:, :, 2]

    return np.clip(label_mask, 0.0, 1.0), (size_x * 0.5, size_y * 0.5, size_z * 0.5)


def get_central_label(map, peak_coordinates):
    th_map = np.where(map == 0.0, 2.0, 1.0)  # shift the thresholding, otherwise only 1 label is found
    labeled_mask = measure.label(th_map, connectivity=1)
    central_label = labeled_mask[peak_coordinates[0], peak_coordinates[1], peak_coordinates[2]]
    labeled_mask = np.where(labeled_mask == central_label, 1.0, 0.0)

    profile_x = np.nonzero(labeled_mask[:, peak_coordinates[1], peak_coordinates[2]])[0]
    profile_y = np.nonzero(labeled_mask[peak_coordinates[0], :, peak_coordinates[2]])[0]
    profile_z = np.nonzero(labeled_mask[peak_coordinates[0], peak_coordinates[1], :])[0]
    size_x = profile_x[-1] - profile_x[0] + 1
    size_y = profile_y[-1] - profile_y[0] + 1
    size_z = profile_z[-1] - profile_z[0] + 1

    return labeled_mask, (size_x, size_y, size_z)


def evaluate_scores_map(input_map, label_type="plane", threshold_type="gauss"):
    pc, ph, slices = create_starting_parameters_2D(input_map)

    if threshold_type == "triangle":
        th = compute_scores_map_threshold_triangle(input_map)
        th = th + np.std(input_map)
    elif threshold_type == "gauss":
        th = compute_gaussian_threshold(input_map)
        th = th - np.std(input_map)
    elif threshold_type == "hard":
        th = ph / 2.0
    else:
        raise ValueError("Unknown type of threshold!")

    th_map = np.where(input_map > th, 1.0, 0.0)
    # th_map_close = binary_closing(th_map)
    th_map = input_map * th_map

    if label_type == "ellipsoid":
        labeled_mask, sizes, surface, th_map = get_ellipsoid_label(th_map, pc)
        labeled_map = labeled_mask * input_map
    elif label_type == "plane":
        labeled_mask, sizes = get_central_plane_labels(th_map, pc)
        labeled_map = labeled_mask * input_map
        surface = []
    else:
        labeled_mask, sizes = get_central_label(th_map, pc)
        labeled_map = labeled_mask * input_map
        surface = []

    return labeled_map, sizes, ph, th_map, surface


def filter_dist_maps(dist_maps, th_mask, min_angles_voxel_count):
    for j in range(dist_maps.shape[3]):
        dist_maps[:, :, :, j] *= th_mask
        dist_label = measure.label(dist_maps[:, :, :, j], connectivity=1)
        dist_props = pd.DataFrame(measure.regionprops_table(dist_label, properties=("label", "area")))
        too_small_dist = dist_props.loc[dist_props["area"] < min_angles_voxel_count, "label"].values
        th_mask = np.where(np.isin(dist_label, too_small_dist), 0.0, dist_label)
        th_mask = np.where(th_mask > 0.0, 1.0, 0.0)
        dist_maps[:, :, :, j] *= th_mask

    for j in range(dist_maps.shape[3]):
        dist_maps[:, :, :, j] *= th_mask

    return dist_maps, th_mask


def create_angular_distance_maps(angles_map, angles_list, output_file_base=None, write_out_maps=True, c_symmetry=1):
    if output_file_base is None:
        if isinstance(angles_map, str):
            output_file_base = angles_map[:-3]
        elif write_out_maps:
            ValueError("The output_file_base was not specified -> the maps will not be written out!")
            write_out_maps = False

    angles_map = cryomap.read(angles_map).astype(int)

    map_shape = angles_map.shape
    angles = geom.load_angles(angles_list)

    zero_rotations = np.tile(angles[0, :], (angles.shape[0], 1))
    dist_all, dist_normals, dist_inplane = geom.compare_rotations(zero_rotations, angles, c_symmetry)

    angles_array = angles_map.flatten() - 1

    ang_dist_map = dist_all[angles_array].reshape(map_shape)
    dist_normals_map = dist_normals[angles_array].reshape(map_shape)
    dist_inplane_map = dist_inplane[angles_array].reshape(map_shape)

    if write_out_maps:
        cryomap.write(ang_dist_map, output_file_base + "_dist_all.em", data_type=np.single)
        cryomap.write(dist_normals_map, output_file_base + "_dist_normals.em", data_type=np.single)
        cryomap.write(dist_inplane_map, output_file_base + "_dist_inplane.em", data_type=np.single)

    return ang_dist_map, dist_normals_map, dist_inplane_map


def select_peaks(
    scores_map,
    angles_map,
    angles_file,
    peak_number=None,
    create_dist_maps=False,
    dist_maps_list=["_dist_all", "_dist_normals", "_dist_inplane"],
    dist_maps_name_base=None,
    write_dist_maps=False,
    min_peak_voxel_count=7,
    min_angles_voxel_count=7,
    template_mask=None,
    template_radius=2,
    edge_masking=None,
    tomo_mask=None,
    output_motl_name=None,
    tomo_number=None,
):
    """Automatic peak selection.

    Parameters
    ----------
    scores_map : ndarray or str
        Map with CCC scores (either path to it or loaded as ndarray)
    angles_map : ndarray or str
        Map with angle indices (either path to it or loaded as ndarray)
    angles_file : ndarray or str
        Angle list used in TM (either path to it or loaded as ndarray). If ndarray is provided it has to be in correct order - phi, theta, psi
    peak_number : int
        Number of peaks to return. Defaults to None.
    create_dist_maps : bool
        Whether to create distance maps. They have to be provided for the computation. Defaults to False.
    dist_maps_list : list
        What distance map(s) to use for the analysis. At least one has to be specified. Defaults to all of them: ['_dist_all','_dist_normals','_dist_inplane'].
    dist_maps_name_base : str
        Path and base name of the distance maps. Defaults to None.
    write_dist_maps : bool
        Whether to write the created distance maps or not. Used only if create_dist_maps is True. Defaults to False.
    min_peak_voxel_count : int
        Size of the minimum volume each peak should have (in voxels). Defaults to 7.
    min_angles_voxel_count : int
        Size of the minimum volume each distance map should have around each peak (in voxels). Defaults to 7.
    template_mask : ndarray or str
        Mask for masking out the volume around the seleceted peak (either path to it or loaded as ndarray). Ideally a tight mask with hard edges, that is NOT hollow (even for hollow structures). Defaults to None.
    template_radius : int
        The radius of a sphere to use for masking out the volume around the selected peak. Used only if the template mask is not specified. Defaults to 2.
    edge_masking : int or ndarray of shape (3
        Dimensions of edges to mask out (). Defaults to None.
    tomo_mask : ndarray
        Mask to exclude regions from the analysis. It has to be the same size as the scores map. Defaults to None.
    output_motl_name : str
        Name of the output motl. Defaults to None which results in no motl to be written out.
    tomo_number : int
        Number of tomogram to be stored in motl. Defaults to None.
    "_dist_normals" :

    "_dist_inplane"] :


    Returns
    -------
    output_motl : cryomotl.Motl
        Motl with the selected peaks.
    empty_label : ndarray
        Map with the selected peaks (same size as scores map).

    Raises
    ------
    ValueError
        If the edge_masking is not specified as one number nor ndsarray of shape (3,)
    ValueError
        If the dist_maps_list contains unknown dist map specifier
    ValueError
        If the create_dist_maps is False and the dist_maps_name_base is not specified

    """

    # load the angles
    angles = geom.load_angles(angles_file)
    angles_map = (cryomap.read(angles_map) - 1).astype(int)

    # get threshold and threshold map
    scores_map = cryomap.read(scores_map)
    th = compute_scores_map_threshold_triangle(scores_map)
    th_map = np.where(scores_map >= th, 1.0, 0.0)

    if tomo_mask is not None:
        th_map *= tomo_mask

    if edge_masking is not None:
        edge_mask = np.zeros(th_map.shape)

        if isinstance(edge_masking, int):
            edge_masking = np.full((3,), edge_masking)
        elif edge_masking.shape[0] != 3:
            raise ValueError("The edge mask has to be single number or 3 numbers - one for each dimension.")
        edge_mask[
            edge_masking[0] : -edge_masking[0], edge_masking[1] : -edge_masking[1], edge_masking[2] : -edge_masking[2]
        ] = 1
        th_map *= edge_mask

    n_dist_maps = len(dist_maps_list)
    dist_maps = np.zeros((th_map.shape[0], th_map.shape[1], th_map.shape[2], n_dist_maps))

    if create_dist_maps:
        temp_dist_maps = create_angular_distance_maps(
            angles_map, angles_file, output_file_base=dist_maps_name_base, write_out_maps=write_dist_maps
        )
        for j, d_name in enumerate(dist_maps_list):
            if d_name == "_dist_all":
                dist_maps[:, :, :, j] = temp_dist_maps[0]
            elif d_name == "_dist_normals":
                dist_maps[:, :, :, j] = temp_dist_maps[1]
            elif d_name == "_dist_inplane":
                dist_maps[:, :, :, j] = temp_dist_maps[2]
            else:
                raise ValueError(f"The dist_maps_list contains unknown dist map specifier: {d_name}!")
    elif dist_maps_name_base is None:
        raise ValueError("The dist_maps_name_base was not specified!")
    else:
        for j, d_name in enumerate(dist_maps_list):
            dist_maps[:, :, :, j] = cryomap.read(dist_maps_name_base + d_name + ".em")

    th_map_d = th_map

    labels = measure.label(th_map, connectivity=1)
    props = pd.DataFrame(measure.regionprops_table(labels, properties=("label", "area")))

    too_small_peaks = props.loc[props["area"] < min_peak_voxel_count, "label"].values
    th_map = np.where(np.isin(labels, too_small_peaks), 0.0, labels)
    th_map = np.where(th_map > 0.0, 1.0, 0.0)

    dist_maps, th_map_d = filter_dist_maps(dist_maps, th_map_d, min_angles_voxel_count)

    for j in range(n_dist_maps):
        dist_temp = np.zeros(th_map.shape)
        dist_label = measure.label(dist_maps[:, :, :, j], connectivity=1)
        dist_props = pd.DataFrame(measure.regionprops_table(dist_label, properties=("label", "bbox")))
        labels, xs, xe, ys, ye, zs, ze = dist_props[
            ["label", "bbox-0", "bbox-3", "bbox-1", "bbox-4", "bbox-2", "bbox-5"]
        ].T.to_numpy()
        for l in range(labels.shape[0]):
            label_cut = dist_label[xs[l] : xe[l], ys[l] : ye[l], zs[l] : ze[l]]
            label_cut = np.where(label_cut == labels[l], 1.0, 0.0)
            label_open = morphology.binary_opening(label_cut, footprint=np.ones((2, 2, 2)), out=None)
            dist_temp[xs[l] : xe[l], ys[l] : ye[l], zs[l] : ze[l]] = np.where(
                label_open == 1, dist_maps[xs[l] : xe[l], ys[l] : ye[l], zs[l] : ze[l], j], 0.0
            )
        dist_maps[:, :, :, j] = dist_temp

    dist_maps, th_map_d = filter_dist_maps(dist_maps, th_map_d, min_angles_voxel_count)

    th_map *= th_map_d

    scores_th = np.ndarray.flatten(scores_map * th_map)
    nz_idx = np.flatnonzero(scores_th)
    remaining_idx = nz_idx[np.argsort(scores_th[nz_idx], axis=None)][::-1]
    selected_peaks = []
    n_selected_peaks = 0

    if template_mask is None:
        particle_mask = cryomask.spherical_mask(2 * template_radius + 2, radius=template_radius)
    else:
        particle_mask = cryomap.read(template_mask)

    if peak_number is None:
        peak_number = remaining_idx.size

    c_idx = 0

    empty_label = np.zeros(th_map.shape)
    removed_idx = []

    c_coord = (np.ceil(np.asarray(particle_mask.shape) / 2)).astype(int)

    while n_selected_peaks < peak_number and remaining_idx.size != 0:
        idx_3d = np.unravel_index(remaining_idx[c_idx], th_map.shape)
        ls, le, ms, me = cryomap.get_start_end_indices(idx_3d, empty_label.shape, particle_mask.shape)
        cut_coord = c_coord - ms

        if template_mask is not None:
            p_particle = cryomap.rotate(
                particle_mask, rotation_angles=angles[angles_map[idx_3d[0], idx_3d[1], idx_3d[2]]]
            )
            p_particle = np.where(p_particle >= 0.5, 1.0, 0.0)
            p_particle = p_particle[ms[0] : me[0], ms[1] : me[1], ms[2] : me[2]]
        else:
            p_particle = particle_mask[ms[0] : me[0], ms[1] : me[1], ms[2] : me[2]]

        overlap_voxels = np.count_nonzero(empty_label[ls[0] : le[0], ls[1] : le[1], ls[2] : le[2]] * p_particle)

        if overlap_voxels == 0 and np.all(cut_coord < me):
            th_label = measure.label(th_map[ls[0] : le[0], ls[1] : le[1], ls[2] : le[2]] * p_particle)
            th_label_id = th_label[cut_coord[0], cut_coord[1], cut_coord[2]]

            if th_label_id == 0:
                peak_area = 0
                angle_size = 0
                print(idx_3d)
            else:
                peak_area = np.count_nonzero(np.where(th_label == th_label_id, 1.0, 0.0))
                angle_size = min_angles_voxel_count
                for j in range(n_dist_maps):
                    dist_label = measure.label(dist_maps[ls[0] : le[0], ls[1] : le[1], ls[2] : le[2], j] * p_particle)
                    dist_label_id = dist_label[cut_coord[0], cut_coord[1], cut_coord[2]]
                    if dist_label_id == 0:
                        angle_size = 0
                        print(idx_3d)
                        break
                    else:
                        ## Add opening
                        label_open = np.where(dist_label == dist_label_id, 1.0, 0.0)
                        # label_open = morphology.binary_opening(label_open, footprint=np.ones((2,2,2)), out=None)
                        # label_open = measure.label(label_open)
                        # open_label_id = label_open[cut_coord[0],cut_coord[1],cut_coord[2]]
                        # label_open = np.where(label_open==open_label_id,1.0,0.0)
                        # if open_label_id == 0:
                        #    angle_size = 0
                        #    break
                        angle_size = np.minimum(angle_size, np.count_nonzero(label_open))
                        if angle_size < min_angles_voxel_count:
                            break

            if angle_size >= min_angles_voxel_count and peak_area >= min_peak_voxel_count:
                empty_label[ls[0] : le[0], ls[1] : le[1], ls[2] : le[2]] += p_particle
                th_map[ls[0] : le[0], ls[1] : le[1], ls[2] : le[2]] = np.where(
                    p_particle == 1, 0.0, th_map[ls[0] : le[0], ls[1] : le[1], ls[2] : le[2]]
                )
                for j in range(n_dist_maps):
                    dist_maps[ls[0] : le[0], ls[1] : le[1], ls[2] : le[2], j] = np.where(
                        p_particle == 1, 0.0, dist_maps[ls[0] : le[0], ls[1] : le[1], ls[2] : le[2], j]
                    )

                selected_peaks.append(
                    (
                        idx_3d,
                        angles[angles_map[idx_3d[0], idx_3d[1], idx_3d[2]]],
                        scores_map[idx_3d[0], idx_3d[1], idx_3d[2]],
                    )
                )
                n_selected_peaks += 1
                non_zero = np.flatnonzero(empty_label)
                remaining_idx = np.setdiff1d(remaining_idx, non_zero, assume_unique=True)
                removed_idx = []
                c_idx = 0
            else:
                removed_idx.append(remaining_idx[c_idx])
                c_idx += 1

        else:
            removed_idx.append(remaining_idx[c_idx])
            c_idx += 1

        if c_idx == remaining_idx.size:
            remaining_idx = np.setdiff1d(remaining_idx, np.asarray(removed_idx), assume_unique=True)
            removed_idx = []
            c_idx = 0

    motl_df = cryomotl.Motl.create_empty_motl_df()
    dim, angles, score = zip(*selected_peaks)
    motl_df[["x", "y", "z"]] = np.array(dim)
    motl_df[["phi", "theta", "psi"]] = np.array(angles)
    motl_df["score"] = score
    motl_df = motl_df.fillna(0)

    if tomo_number is not None:
        motl_df["tomo_id"] = tomo_number

    motl_df["subtomo_id"] = range(1, len(selected_peaks) + 1)
    motl_df["class"] = 1

    output_motl = cryomotl.Motl(motl_df)

    if output_motl_name is not None:
        output_motl.write_to_emfile(output_motl_name)

    print(f"Number of selected peaks: {output_motl.df.shape[0]}")

    return output_motl, empty_label
