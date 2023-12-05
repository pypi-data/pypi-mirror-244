import open3d as o3d
import numpy as np
from ..common.common_utils import color_rings7_det as colormap

def create_cloud(filepath, filetype='pcd', num_features=4):
    cloud = o3d.geometry.PointCloud()
    if filetype == "bin":
        points = np.fromfile(filepath, dtype=np.float32).reshape(-1, num_features)[:, :3]
        cloud.points = o3d.utility.Vector3dVector(points[:, :3])
        # 手动计算填入到 cloud.colors 来为每个点着色
    elif filetype == "pcd":
        cloud.points = o3d.io.read_point_cloud(filepath).points
    elif filetype == "npy":
        points = np.load(filepath)[:, :3]
        cloud.points = o3d.utility.Vector3dVector(points[:, :3])
    else:
        print("unsupport file type")

    return cloud

def playcloud(point_clouds, start=0, step=10, bboxes_3d=None, 
              color=None, point_size=None,
              ):
    def switch(vis, i):
        pc = point_clouds[i]
        print(f"frame {i}: {pc['filepath']}")
        cloud = create_cloud(pc['filepath'], pc['filetype'], num_features=pc['num_features'])
        if color: cloud.paint_uniform_color(color)
        if point_size: vis.get_render_option().point_size = point_size

        vis.clear_geometries()
        # vis.update_geometry(cloud)
        vis.add_geometry(cloud) # 离谱 update 没用，add 反而有效
        
        if bboxes_3d and bboxes_3d[i]: o3d_draw_boxes(vis, bboxes_3d[i])
        
        # vis.poll_events()
        vis.update_renderer()

    def prev(vis):
        global g_idx
        g_idx = max(g_idx - 1, 0)
        switch(vis, g_idx)
    def next(vis):
        global g_idx
        g_idx = min(g_idx + 1, len(point_clouds)-1)
        switch(vis, g_idx)
    def prev_n(vis):
        global g_idx
        g_idx = max(g_idx - step, 0)
        switch(vis, g_idx)
    def next_n(vis):
        global g_idx
        g_idx = min(g_idx + step, len(point_clouds)-1)
        switch(vis, g_idx)

    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window()
    vis.get_render_option().point_size = 1.0
    vis.get_render_option().background_color = np.zeros(3)

    vis.register_key_callback(ord('W'), prev_n) 
    vis.register_key_callback(ord('S'), next_n)
    vis.register_key_callback(ord('A'), prev) 
    vis.register_key_callback(ord('D'), next) # 按小写，但这里要填大写
    # vis.register_key_callback(ord(' '), next) # space

    global g_idx
    g_idx = start
    switch(vis, start)
    vis.run()
    vis.destroy_window()

def translate_boxes_to_open3d_instance(box):
    """
             4-------- 6
           /|         /|
          5 -------- 3 .
          | |        | |
          . 7 -------- 1
          |/         |/
          2 -------- 0
    """
    rot = o3d.geometry.get_rotation_matrix_from_axis_angle(box['axis_angles'])
    box3d = o3d.geometry.OrientedBoundingBox(box['location'], rot, box['dimensions'])

    line_set = o3d.geometry.LineSet.create_from_oriented_bounding_box(box3d)

    lines = np.asarray(line_set.lines)
    lines = np.concatenate([lines, np.array([[1, 4], [7, 6]])], axis=0)

    line_set.lines = o3d.utility.Vector2iVector(lines)

    return line_set, box3d

def o3d_draw_boxes(vis, bboxes_3d):
    # 坐标轴
    axis_pcd = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0, origin=[0, 0, 0])
    vis.add_geometry(axis_pcd)
    # 包围盒
    for box in bboxes_3d:
        line_set, box3d = translate_boxes_to_open3d_instance(box)
        line_set.paint_uniform_color(colormap[box['label']])
        vis.add_geometry(line_set) # 线框
        # vis.add_geometry(box3d) # 立方体
