from . import config
from .common_utils import transform_matrix
import pickle
import numpy as np
from pyquaternion import Quaternion


def decode_kitti_infos(pkl, valid_classes, filetype="bin", num_features=4, **kwargs):
    map_cls_name2id = {cls:i for i, cls in enumerate(valid_classes)}
    bboxes_3d, point_clouds, images = [], [], []
    with open(pkl, 'rb') as f:
        infos = pickle.load(f)
    split = "training" if ("train" in pkl or "val" in pkl) else "testing"
    for info in infos:
        frame_id = info['point_cloud']['lidar_idx']
        cloudpath = f"{split}/velodyne/{frame_id}.bin"
        point_clouds.append({
            'filepath': cloudpath,
            'filetype': filetype,
            'num_features': num_features,
            'frame_id': frame_id,
        })
        
        imagepath = f"{split}/image_2/{info['image']['image_idx']}.png"
        lidar2pixel_mat = info['calib']['P2'] @ info['calib']['R0_rect'] @ info['calib']['Tr_velo_to_cam']
        images.append({
            'image_2': {
                'filepath': imagepath,
                'calib': {'l2p_tm': lidar2pixel_mat},
            },
        })

        if 'annos' in info:
            name = info['annos']['name']
            bboxes_3d_frame = []
            for i in range(len(name)):
                if name[i] in valid_classes:
                    gt_boxes = info['annos']['gt_boxes_lidar'][i]
                    ext_info = {
                        'difficulty': info['annos']['difficulty'][i],
                        'num_points': info['annos']['num_points_in_gt'][i],
                        'occluded': info['annos']['occluded'][i],
                        'truncated': info['annos']['truncated'][i],
                    }

                    bboxes_3d_frame.append({
                        'location': gt_boxes[0:3],
                        'dimensions': gt_boxes[3:6],
                        'axis_angles': np.array([0, 0, gt_boxes[6] + 1e-10]),
                        'label': map_cls_name2id[name[i]],
                        'ext_info': ext_info,
                    })

            bboxes_3d.append(bboxes_3d_frame)
        else:
            bboxes_3d.append(None)
    
    info_dict = {'point_clouds': point_clouds, 'bboxes_3d': bboxes_3d, 'images': images,
                 'metainfo': {'categories': map_cls_name2id, 'cams': ['image_2']},
                 }

    return info_dict
def decode_nuscenes_infos(pkl, valid_classes, filetype="bin", num_features=5, add_ext_info=False):
    map_cls_name2id = {cls:i for i, cls in enumerate(valid_classes)}
    bboxes_3d, point_clouds, images = [], [], []
    with open(pkl, 'rb') as f:
        infos = pickle.load(f)

    for info in infos:
        point_clouds.append({
            'filepath': info['lidar_path'],
            'filetype': filetype,
            'num_features': num_features,
        })

        image_dict = {}
        e2l_mat = info['ref_from_car']
        g2e_lidar_mat = info['car_from_global']
        l2e_mat = transform_matrix(e2l_mat[:3, :3], e2l_mat[:3, 3], inverse=True)
        e2g_lidar_mat = transform_matrix(g2e_lidar_mat[:3, :3], g2e_lidar_mat[:3, 3], inverse=True)
        for key, cam in info['cams'].items():

            intrinsics_4x4 = np.eye(4)
            intrinsics_4x4[:3, :3] = cam['camera_intrinsics']
            c2e_mat_inv = transform_matrix(Quaternion(cam['sensor2ego_rotation']).rotation_matrix, np.array(cam['sensor2ego_translation']), inverse=True)
            e2g_cam_mat_inv = transform_matrix(Quaternion(cam['ego2global_rotation']).rotation_matrix, np.array(cam['ego2global_translation']), inverse=True)

            lidar2pixel_mat = intrinsics_4x4 @ c2e_mat_inv @ e2g_cam_mat_inv @ e2g_lidar_mat @ l2e_mat

            image_dict[key] = {
                'filepath': cam['data_path'],
                'calib': {'l2p_tm': lidar2pixel_mat},
            }

        images.append(image_dict)
        
        if 'gt_boxes' in info:
            name = info['gt_names']
            bboxes_3d_frame = []
            for i in range(len(name)):
                if name[i] in valid_classes:
                    gt_boxes = info['gt_boxes'][i]
                    ext_info = {
                        'num_points': info['num_lidar_pts'][i],
                    }
                    bboxes_3d_frame.append({
                        'location': gt_boxes[0:3],
                        'dimensions': gt_boxes[3:6],
                        'axis_angles': np.array([0, 0, gt_boxes[6] + 1e-10]),
                        'label': map_cls_name2id[name[i]],
                        'ext_info': ext_info,
                    })

            bboxes_3d.append(bboxes_3d_frame)
        else:
            bboxes_3d.append(None)
        
    if add_ext_info:
        from nuscenes.nuscenes import NuScenes
        version = "v1.0-trainval"
        nusc = NuScenes(version=version, dataroot=config.nus_root, verbose=True)
        # 添加场景描述信息用于可视化时，过滤样本
        for i, info in enumerate(infos):
            sample_token = info['token']
            sample = nusc.get('sample', sample_token)
            scene = nusc.get('scene', sample['scene_token'])
            point_clouds[i]['ext_info'] = {'desc': scene['description'].lower()}

    info_dict = {'point_clouds': point_clouds, 'bboxes_3d': bboxes_3d, 'images': images,
                 'metainfo': {'categories': map_cls_name2id, 'cams': list(infos[0]['cams'].keys())},
                 }

    return info_dict


def decode_kitti_eval(eval_pkl, gt_pkl):
    with open(eval_pkl, 'rb') as f:
        eval_infos = pickle.load(f)
    with open(gt_pkl, 'rb') as f:
        gt_infos = pickle.load(f)

    lut = {gt_infos['point_clouds'][i]['frame_id']:i for i in range(len(gt_infos['point_clouds']))}
    map_cls_name2id = gt_infos['metainfo']['categories']

    point_clouds, bboxes_3d, images = [], [], []
    for eval_info in eval_infos:
        eval_box3d_frame = []
        for j in range(len(eval_info['name'])):
            eval_box3d_frame.append({
                'location': eval_info['boxes_lidar'][j][:3],
                'dimensions': eval_info['boxes_lidar'][j][3:6],
                'axis_angles': np.array([0, 0, eval_info['boxes_lidar'][j][6] + 1e-10]),
                'label': map_cls_name2id[eval_info['name'][j]],
                'ext_info': {'score': eval_info['score'][j]},
            })

        gt_idx = lut[eval_info['frame_id']]
        for j in range(len(gt_infos['bboxes_3d'][gt_idx])):
            gt_infos['bboxes_3d'][gt_idx][j]['label'] = -1
        gt_infos['bboxes_3d'][gt_idx].extend(eval_box3d_frame)

        point_clouds.append(gt_infos['point_clouds'][gt_idx])
        bboxes_3d.append(gt_infos['bboxes_3d'][gt_idx])
        images.append(gt_infos['images'][gt_idx])

    info_dict = {'point_clouds': point_clouds, 'bboxes_3d': bboxes_3d, 'images': images,
                 'metainfo': gt_infos['metainfo'],
                 }

    return info_dict
