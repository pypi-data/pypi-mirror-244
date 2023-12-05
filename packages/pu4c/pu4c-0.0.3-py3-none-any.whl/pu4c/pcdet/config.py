
kitti_root = "/datasets/KITTI/object"
kitti_classes = ['Car', 'Pedestrian', 'Cyclist', 'Van', 'Truck', 'Person_sitting', 'Tram', 'Misc', 'DontCare']
kitti_info_pkls = [
    "/datasets/blob/pcdet/data/kitti/kitti_infos_train.pkl", 
    "/datasets/blob/pcdet/data/kitti/kitti_infos_val.pkl", 
    "/datasets/blob/pcdet/data/kitti/kitti_infos_test.pkl",
    ]
kitti_vis_info_pkls = [
    "/datasets/blob/pu4c/kitti_vis_infos_train.pkl", 
    "/datasets/blob/pu4c/kitti_vis_infos_val.pkl", 
]

nus_root = "/datasets/nuScenes/Fulldatasetv1.0"
nus_classes = ['car', 'pedestrian', 'bicycle', 'motorcycle', 'bus', 'truck', 
               'construction_vehicle', 'trailer', 'barrier', 'traffic_cone', 'ignore']
nus_info_pkls = [
    "/datasets/blob/pcdet/data/nuscenes/v1.0-trainval/nuscenes_infos_10sweeps_train.pkl", 
    "/datasets/blob/pcdet/data/nuscenes/v1.0-trainval/nuscenes_infos_10sweeps_val.pkl",
    ]
nus_vis_info_pkls = [
    "/datasets/blob/pu4c/nuscenes_vis_infos_10sweeps_train.pkl", 
    "/datasets/blob/pu4c/nuscenes_vis_infos_10sweeps_val.pkl",
    ]


waymo_root = "/datasets/blob/pcdet/data/waymo/waymo_processed_data"
waymo_info_pkls = [
    "/datasets/blob/pcdet/data/waymo/waymo_infos_train.pkl", 
    "/datasets/blob/pcdet/data/waymo/waymo_infos_val.pkl",
    ]


