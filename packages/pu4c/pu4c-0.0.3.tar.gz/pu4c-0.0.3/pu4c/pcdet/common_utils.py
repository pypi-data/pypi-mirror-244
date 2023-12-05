import numpy as np

def project_points_to_pixels(points, image, transform_mat):
    """
    y = Rx 即 y(4,N) = transform_mat @ (4, N) 即 y(N,4) = (N,4) @ transform_mat.T
    """
    points_hom = np.hstack((points[:, :3], np.ones((points.shape[0], 1), dtype=np.float32))) # [N, 4]
    points_cam = (points_hom @ transform_mat.T)[:, :3]
    
    pixels_depth = points_cam[:, 2]
    pixels = (points_cam[:, :2].T / points_cam[:, 2]).T # (N, 2)[col, row]

    # remove points outside the image
    mask = pixels_depth > 0
    mask = np.logical_and(mask, pixels[:, 0] > 0)
    mask = np.logical_and(mask, pixels[:, 0] < image.shape[1])
    mask = np.logical_and(mask, pixels[:, 1] > 0)
    mask = np.logical_and(mask, pixels[:, 1] < image.shape[0])

    return pixels, pixels_depth, mask

def get_oriented_bounding_box_corners(xyz, lwh, axis_angles):
    """
        轴角转旋转矩阵（暂只考虑偏航）来将其旋转为有向包围盒，计算盒子的 8 个角点，添加连线
        Locals:
            lines: (10, 2), 预定义的 14 条连线
            4-------- 6
        /|         /|
        5 -------- 3 .
        | |        | |
        . 7 -------- 1          
        |/         |/       z |/ x  
        2 -------- 0      y - 0
        Returns:
            corners: (N, 8, 3)
    """
    x, y, z = xyz
    l, w, h = lwh
    roll, pitch, yaw = axis_angles
    xdif, ydif, zdif = l/2, w/2, h/2
    offsets = np.array([
        [-xdif,  xdif, -xdif, -xdif, xdif, -xdif,  xdif,  xdif],
        [-ydif, -ydif,  ydif, -ydif, ydif,  ydif, -ydif,  ydif],
        [-zdif, -zdif, -zdif,  zdif, zdif,  zdif,  zdif, -zdif],
    ])
    R_x = np.array([
        [ 1, 0            ,  0          ],
        [ 0, np.cos(roll) , -np.sin(roll)],
        [ 0, np.sin(roll) ,  np.cos(roll)],
    ])
    R_y = np.array([
        [ np.cos(pitch),  0,  np.sin(pitch)],
        [ 0            ,  1,  0            ],
        [-np.sin(pitch),  0,  np.cos(pitch)],
    ])
    R_z = np.array([
        [ np.cos(yaw), -np.sin(yaw),  0],
        [ np.sin(yaw),  np.cos(yaw),  0],
        [ 0          ,  0          ,  1],
    ])
    R = R_x @ R_y @ R_z
    corners = (R @ offsets + np.array([[x], [y], [z]])).T
    
    return corners

def get_oriented_bounding_box_lines(head_cross_lines=True):
    lines = [
                [0, 2], [0, 3], [2, 5], [3, 5],
                [0, 1], [3, 6], [5, 4], [2, 7],
                [1, 6], [1, 7], [7, 4], [4, 6],
            ]
    if head_cross_lines:
        lines.extend([[1, 4], [6, 7]])
    return lines

# TODO
def get_range_image(points):
    pass 

def transform_matrix(rotation_mat, translation, inverse: bool = False) -> np.ndarray:
    """
    返回变换矩阵或变换矩阵的逆，直接对变换矩阵求逆可能无解报错
    """
    tm = np.eye(4)

    if inverse:
        rot_inv = rotation_mat.T
        trans = np.transpose(-np.array(translation))
        tm[:3, :3] = rot_inv
        tm[:3, 3] = rot_inv.dot(trans)
    else:
        tm[:3, :3] = rotation_mat
        tm[:3, 3] = np.transpose(np.array(translation))

    return tm