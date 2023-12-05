
from ..common.common_utils import limit_period
import pickle
import numpy as np


def decode_waymo_infos(fname, valid_classes, filetype="bin", num_features=6, add_ext_info=False):
    map_cls_name2id = {cls:i for i, cls in enumerate(valid_classes)}
    map_cam_name2id = {'CAM_FRONT': 0, 'CAM_FRONT_LEFT': 1, 'CAM_FRONT_RIGHT': 2, 'CAM_SIDE_LEFT': 3, 'CAM_SIDE_RIGHT': 4}
    map_cam_id2name = {v: k for k, v in map_cam_name2id.items()}
    bboxes_3d, point_clouds, images = [], [], []
    with open(fname, 'rb') as f:
        infos = pickle.load(f)

    spilt = "training" if ("train" in fname or "val" in fname) else "testing"
    cat_map = {v: k for k, v in infos['metainfo']['categories'].items()}
    for info in infos['data_list']:
    # for info in infos['data_list'][:10]:
        cloudpath = f"{spilt}/velodyne/{info['lidar_points']['lidar_path']}"
        point_clouds.append({
            'filepath': cloudpath,
            'filetype': filetype,
            'num_features': num_features,
            'frame_id': info['sample_idx'],
        })
        
        image_dict = {}
        for key, cam in info['images'].items():
            img_ix = f"image_{map_cam_name2id[key]}"
            imagepath = f"{spilt}/{img_ix}/{cam['img_path']}"

            lidar2pixel_mat = np.array(cam['lidar2img'])
            image_dict[key] = {
                'filepath': imagepath,
                'calib': {'l2p_tm': lidar2pixel_mat},
            }

        images.append(image_dict)
        
        bboxes_3d_frame = [] if len(info['instances']) > 0 else None
        for instance in info['instances']:
            name = cat_map[instance['bbox_label_3d']]
            if name in map_cls_name2id.keys():
                ext_info = {
                    'difficulty': instance['difficulty'],
                }
                # 3D 框需要计算，参考 WaymoDataset.parse_ann_info/CameraInstance3DBoxes.convert_to
                # camera_name = map_cam_id2name[int(instance['camera_id'])] # 用每个相机自己的矩阵反而是错了
                # lidar2cam = np.array(info['images'][camera_name]['lidar2cam'])
                lidar2cam = np.array(info['images']['CAM_FRONT']['lidar2cam'])
                cam2lidar = np.linalg.inv(lidar2cam)

                # box 转坐标系还挺麻烦
                gt_boxes_cam = instance['bbox_3d']
                xyz_ext = np.ones(4)
                xyz_ext[:3] = gt_boxes_cam[:3]
                xyz_ext = xyz_ext @ cam2lidar.T
                # % 这里注意相机坐标系转雷达坐标系，坐标轴要变
                xyz_size = np.array([gt_boxes_cam[3], gt_boxes_cam[5], gt_boxes_cam[4]])
                yaw = limit_period(-gt_boxes_cam[6] - np.pi / 2, period=np.pi * 2)

                # mmdet3d 中似乎有 bug，没对 z 纠正导致框高度上有偏移
                xyz_ext[2] = xyz_ext[2] + (xyz_size[2] / 2)
                ext_info = {
                    'num_points': instance['num_lidar_pts'],
                }
                bboxes_3d_frame.append({
                    'location': xyz_ext[:3],
                    'dimensions': xyz_size,
                    'axis_angles': np.array([0, 0, yaw + 1e-10]),
                    'label': map_cls_name2id[name],
                    'ext_info': ext_info,
                })

        bboxes_3d.append(bboxes_3d_frame)
    
    if add_ext_info:
        import os
        from . import config

        waymo_ext_info_pkl = config.waymo_ext_info_pkls[0] if 'train' in fname else config.waymo_ext_info_pkls[1]
        if os.path.exists(waymo_ext_info_pkl):
            print(f"file exist: {waymo_ext_info_pkl}")
            with open(waymo_ext_info_pkl, 'rb') as f:
                all_ext_infos = pickle.load(f)
        else:
            from waymo_open_dataset import dataset_pb2
            import tensorflow as tf
            from tqdm import tqdm
            from glob import glob
            key = 'training' if 'train' in fname else 'validation'
            load_dir = f"{config.waymo_raw_root}/{key}"
            tfrecord_pathnames = sorted(glob(os.path.join(load_dir, '*.tfrecord')))
            
            def get_ext_info_sigle(sequence_file):
                dataset = tf.data.TFRecordDataset(str(sequence_file), compression_type='')
                ext_infos = []
                for data in dataset:
                    frame = dataset_pb2.Frame()
                    frame.ParseFromString(bytearray(data.numpy()))
                    time_of_day = frame.context.stats.time_of_day.lower()
                    weather = frame.context.stats.weather.lower()
                    location = frame.context.stats.location.lower()
                    ext_info = {
                        'desc': f"{time_of_day} {weather} {location}"
                    }
                    ext_infos.append(ext_info)
                return ext_infos
            
            num_workers=8
            import concurrent.futures as futures
            with futures.ThreadPoolExecutor(num_workers) as executor:
                ext_infos_list = list(tqdm(executor.map(get_ext_info_sigle, tfrecord_pathnames), total=len(tfrecord_pathnames)))

            all_ext_infos = [ext_info for ext_info_seq in ext_infos_list for ext_info in ext_info_seq]
            with open(waymo_ext_info_pkl, 'wb') as f:
                pickle.dump(all_ext_infos, f)

        assert (len(all_ext_infos) == len(infos['data_list']))
        for i in range(len(all_ext_infos)):
            point_clouds[i]['ext_info'] = all_ext_infos[i]
        
    info_dict = {'point_clouds': point_clouds, 'bboxes_3d': bboxes_3d, 'images': images,
                 'metainfo': {'categories': map_cls_name2id, 'cams': list(info['images'].keys())},
                 }

    return info_dict

