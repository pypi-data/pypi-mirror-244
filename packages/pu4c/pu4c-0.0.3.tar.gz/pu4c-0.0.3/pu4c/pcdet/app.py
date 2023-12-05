from . import config


def playeval(eval_pkl,
             root=config.kitti_root,
             gt_pkl=config.kitti_vis_info_pkls[1],
             start=0, step=10,
             color=None, point_size=1,
             ):
    """
    Visualize the eval result, with the gt box in green
    """
    from .open3d_utils import playcloud
    from .data_utils import decode_kitti_eval

    info_dict = decode_kitti_eval(eval_pkl, gt_pkl)
    for pc in info_dict['point_clouds']:
        pc['filepath'] = f"{root}/{pc['filepath']}"
    playcloud(info_dict['point_clouds'], bboxes_3d=info_dict['bboxes_3d'], start=start, step=step,
              color=color, point_size=point_size,
              )

def create_vis_infos(dataset="kitti"):
    """
    生成用于可视化的数据接口
    """
    from .data_utils import decode_kitti_infos, decode_nuscenes_infos
    from ..mmdet3d.data_utils import decode_waymo_infos
    import pickle
    from ..mmdet3d import config as config_mmdet3d
    default_param_dict = {
        "kitti": [decode_kitti_infos, config.kitti_info_pkls, config.kitti_vis_info_pkls, config.kitti_classes[:3]],
        "nus":   [decode_nuscenes_infos, config.nus_info_pkls, config.nus_vis_info_pkls, config.nus_classes[:4]],
        "waymo": [decode_waymo_infos, config_mmdet3d.waymo_info_pkls, config_mmdet3d.waymo_vis_info_pkls, config_mmdet3d.waymo_kitti_classes[:3]],
    }
    decoder, src_pkls, dst_pkls, valid_classes = default_param_dict[dataset]
    for src_pkl, dst_pkl in zip(src_pkls, dst_pkls):
        info_dict = decoder(src_pkl, valid_classes=valid_classes,
                            add_ext_info=True if dataset in ['nus', 'waymo'] else False
                            )
        print(dst_pkl)
        with open(dst_pkl, 'wb') as f:
            pickle.dump(info_dict, f)
def playdataset(root=config.kitti_root, pkl=config.kitti_vis_info_pkls[0], 
                start=0, step=10,
                color=None, point_size=1,
                help=False,
                ):
    """
    visualize dataset split，A/D switch one frame ; W/S switch ${step} frame; esc to exit
    """
    if help:
        print(
            "pu4c.pcdet.app.playdataset(root=config.nus_root, pkl=config.nus_vis_info_pkls[1])"
            "pu4c.pcdet.app.playdataset(root=config.waymo_root, pkl=config.waymo_vis_info_pkls[1])"
        )
        return
    from .open3d_utils import playcloud
    import pickle
    with open(pkl, 'rb') as f:
        info_dict = pickle.load(f)
    for pc in info_dict['point_clouds']:
        pc['filepath'] = f"{root}/{pc['filepath']}"

    print(f"visualize {pkl}, total {len(info_dict['point_clouds'])} frames")
    playcloud(info_dict['point_clouds'], bboxes_3d=info_dict['bboxes_3d'], start=start, step=step,
              color=color, point_size=point_size,
              )


def cloud_viewer_from_dir(root, pattern="*",
                          filetype="bin", num_features=4, start=0, step=10, 
                          color=None, point_size=1,
                          ):
    """
    Visualize point clouds in a directory
    """
    from .open3d_utils import playcloud
    from glob import glob
    files = sorted(glob(f'{root}/{pattern}'))

    point_clouds = []
    for filepath in files:
        point_clouds.append({
            'filepath': filepath,
            'filetype': filetype,
            'num_features': num_features,
        })
    
    playcloud(point_clouds, start=start, step=step, 
              color=color, point_size=point_size,
              )
def cloud_viewer(filepath, filetype='pcd', num_features=4, point_size=1):
    """
    快速查看单帧点云，支持 pcd/bin/npy
    """
    import open3d as o3d
    from .open3d_utils import create_cloud
    
    vis = o3d.visualization.Visualizer()
    vis.create_window()

    vis.get_render_option().point_size = point_size
    vis.get_render_option().show_coordinate_frame = True

    cloud = create_cloud(filepath, filetype, num_features=num_features)
    vis.add_geometry(cloud)

    vis.run()
    vis.destroy_window()