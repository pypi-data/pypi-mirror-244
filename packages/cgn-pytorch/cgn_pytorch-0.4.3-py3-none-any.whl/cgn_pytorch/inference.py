# Copyright (c) 2023 Sebastian Peralta
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import torch
import meshcat
import cgn_pytorch.util.config_utils as config_utils
import numpy as np
from importlib.resources import files
from torch_geometric.nn import fps as farthest_point_sample
import random
from cgn_pytorch.util.test_meshcat_pcd import meshcat_pcd_show as viz_points
from cgn_pytorch.util.test_meshcat_pcd import sample_grasp_show as viz_grasps
from scipy.spatial.transform import Rotation as R
from cgn_pytorch.contact_graspnet import CGN


def from_pretrained(
    checkpoint_path: str = None, device: [str, int] = 0
) -> tuple[CGN, torch.optim.Adam, dict]:
    """Loads a pretrained model and optimizer.

    Args:

      device ([str,int], optional): The device to load the model on. Defaults to 0.
      checkpoint_path (str, optional): The path to the checkpoint file. If None,
       a pretrained model based on https://github.com/NVlabs/contact_graspnet
         will be loaded.

    Returns:
        tuple[torch.nn.Module, torch.optim.Adam, dict]: CGN model, optimizer and config dict.
    """
    print("Initializing net...")
    torch.cuda.empty_cache()
    config_dict = config_utils.load_config()
    device = torch.device(
        "cuda:0" if torch.cuda.is_available() and device != "cpu" else "cpu"
    )
    model = CGN(config_dict, device).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    if checkpoint_path is None:
        checkpoint_path = files("cgn_pytorch").joinpath("checkpoints/current.pth")
    checkpoint = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(checkpoint["state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer"])
    print("...net initialized.")
    return model, optimizer, config_dict


def visualize_grasps(
    pcd, grasps, mc_vis=None, gripper_depth=0.1034, gripper_width=0.08
):
    print("Visualizing. Run meshcat-server in another terminal to see visualization.")
    if mc_vis is None:
        mc_vis = meshcat.Visualizer(zmq_url="tcp://127.0.0.1:6000")

    viz_points(mc_vis, pcd, name="pointcloud", color=(0, 0, 0), size=0.002)
    grasp_kp = get_key_points(
        grasps, gripper_depth=gripper_depth, gripper_width=gripper_width
    )
    viz_grasps(mc_vis, grasp_kp, name="gripper/", freq=1)


def get_key_points(poses, gripper_depth=0.1034, gripper_width=0.08, symmetric=False):
    gripper_pts = get_control_points(
        gripper_depth, gripper_width, poses.shape[0], symmetric=symmetric
    )
    pts = np.matmul(poses, gripper_pts.transpose(0, 2, 1)).transpose(0, 2, 1)

    return pts


def grasp_to_gripper(grasp_pose, translate=0.0, theta=np.pi / 2):
    """
    does a small conversion between the grasp frame and the actual gripper frame for IK
    """
    z_rot = np.eye(4)
    z_rot[2, 3] = translate
    z_rot[:3, :3] = R.from_euler("z", theta).as_matrix()
    z_tf = np.matmul(z_rot, np.linalg.inv(grasp_pose))
    z_tf = np.matmul(grasp_pose, z_tf)
    gripper_pose = np.matmul(z_tf, grasp_pose)

    return gripper_pose


def get_control_points(
    gripper_depth: float, gripper_width: float, batch_size: int, symmetric: bool = False
) -> np.ndarray:
    """Get the gripper base, finger tips and mid finger points represented as a
        matrix with each row 
    Args:
        gripper_depth (float):
        gripper_width (float):
        batch_size (int): Number of points to return.
        symmetric (bool, optional): Return a symmetric set of control points. Defaults to False.

    Returns:
        np.ndarray: Control points represented as a matrix of shape (batch_size, 4, 4).
    """
    if symmetric:
        control_points = np.asarray(
            [
                [0, 0, 0, 1], # Base of gripper.
                [-gripper_width / 2, gripper_width / 2, 0.75 * gripper_depth, 1],
                [gripper_width / 2, -gripper_width / 2, 0.75 * gripper_depth, 1],
                [-gripper_width / 2, gripper_width / 2, gripper_depth, 1],
                [gripper_width / 2, -gripper_width / 2, gripper_depth, 1],
            ]
        )
    else:
        control_points = np.asarray(
            [
                [0.0, 0.0, 0.0, 1.0],
                [gripper_width / 2, -gripper_width / 2, 0.75 * gripper_depth, 1.0],
                [-gripper_width / 2, gripper_width / 2, 0.75 * gripper_depth, 1.0],
                [gripper_width / 2, -gripper_width / 2, gripper_depth, 1.0],
                [-gripper_width / 2, gripper_width / 2, gripper_depth, 1.0],
            ]
        )

    return np.tile(control_points, [batch_size, 1, 1])


# class CgnInference(torch.nn.Module):
#     """Wraps Cgn with a forward function that takes point clouds and returns a
#     tuple of a list of grasps and a list of the corresponding confidence values.
#     """

#     def __init__(self, cgn: CGN):
#         super().__init__()
#         self.cgn = cgn

#     def forward(self, pcd, threshold=0.5):
#         # if pcd.shape[0] > 20000:
#         #     downsample =torch.tensor(random.sample(range(pcd.shape[0] - 1), 20000))
#         # else:
#         #     downsample = torch.arange(20000)
#         # pcd = pcd[downsample, :]

#         # pcd = torch.Tensor(pcd).to(dtype=torch.float32).to(self.cgn.device)
#         batch = torch.zeros(pcd.shape[0]).to(dtype=torch.int64).to(self.cgn.device)
#         idx = farthest_point_sample(pcd, batch, 2048 / pcd.shape[0])
#         # idx = torch.linspace(0, pcd.shape[0]-1, 2048).to(dtype=torch.int64).to(cgn.device)

#         # obj_mask = torch.ones(idx.shape[0])

#         points, pred_grasps, confidence, pred_widths, _, pred_collide = self.cgn(
#             pcd[:, 3:], pos=pcd[:, :3], batch=batch, idx=idx
#         )
#         sig = torch.nn.Sigmoid()
#         confidence = sig(confidence)
#         confidence = confidence.reshape((-1,))
#         pred_grasps = torch.flatten(pred_grasps, start_dim=0, end_dim=1)
#         # confidence = (obj_mask * confidence).reshape((-1,))
#         pred_widths = torch.flatten(pred_widths, start_dim=0, end_dim=1)
#         points = torch.flatten(points, start_dim=0, end_dim=1)

#         success_mask = (confidence > threshold).nonzero()[0]

#         return pred_grasps[success_mask], confidence[success_mask]


def inference(
    cgn: CGN,
    pcd: np.ndarray,
    threshold: float = 0.5,
    visualize=False,
    max_grasps: int = 0,
    gripper_depth: float = 0.1034,
    gripper_width: float = 0.08,
    obj_mask: np.ndarray = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Infer grasps from a point cloud and optional object mask.

    Args:
        cgn (CGN): ContactGraspNet model
        pcd (np.ndarray): point cloud
        threshold (float, optional): Success threshol. Defaults to 0.5.
        visualize (bool, optional): Whether or not to visualize output. Defaults to False.
        max_grasps (int, optional): Maximum grasps. Zero means unlimited. Defaults to 0.
        obj_mask (np.ndarray, optional): Object mask. Defaults to None.

    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray]: The grasps, confidence and indices of the points used for inference.
    """
    cgn.eval()
    pcd = torch.Tensor(pcd).to(dtype=torch.float32).to(cgn.device)
    if pcd.shape[0] > 20000:
        downsample_idxs = np.array(random.sample(range(pcd.shape[0] - 1), 20000))
    else:
        downsample_idxs = np.arange(pcd.shape[0])
    pcd = pcd[downsample_idxs, :]

    batch = torch.zeros(pcd.shape[0]).to(dtype=torch.int64).to(cgn.device)
    fps_idxs = farthest_point_sample(pcd, batch, 2048 / pcd.shape[0])

    if obj_mask is not None:
        obj_mask = torch.Tensor(obj_mask[downsample_idxs])
        obj_mask = obj_mask[fps_idxs]
    else:
        obj_mask = torch.ones(fps_idxs.shape[0])
    points, pred_grasps, confidence, pred_widths, _, _ = cgn(
        pcd[:, 3:],
        pcd_poses=pcd[:, :3],
        batch=batch,
        idxs=fps_idxs,
        gripper_depth=gripper_depth,
        gripper_width=gripper_width,
    )

    sig = torch.nn.Sigmoid()
    confidence = sig(confidence)
    confidence = confidence.reshape(-1)
    pred_grasps = (
        torch.flatten(pred_grasps, start_dim=0, end_dim=1).detach().cpu().numpy()
    )

    confidence = (
        obj_mask.detach().cpu().numpy() * confidence.detach().cpu().numpy()
    ).reshape(-1)
    pred_widths = (
        torch.flatten(pred_widths, start_dim=0, end_dim=1).detach().cpu().numpy()
    )
    points = torch.flatten(points, start_dim=0, end_dim=1).detach().cpu().numpy()

    success_mask = (confidence > threshold).nonzero()[0]
    if len(success_mask) == 0:
        print("failed to find successful grasps")
        return None, None, None

    success_grasps = pred_grasps[success_mask]
    success_confidence = confidence[success_mask]
    print("Found {} grasps".format(success_grasps.shape[0]))
    if max_grasps > 0 and success_grasps.shape[0] > max_grasps:
        success_grasps = success_grasps[:max_grasps]
        success_confidence = success_confidence[:max_grasps]
    if visualize:
        visualize_grasps(
            pcd.detach().cpu().numpy(),
            success_grasps,
            gripper_depth=gripper_depth,
            gripper_width=gripper_width,
        )
    return success_grasps, success_confidence, downsample_idxs


# def to_onnx(model: CGN, save_path: str = "contact_graspnet.onnx"):
#     dynamic_axes_dict = {
#         "input": {
#             0: "npoints",
#         },
#         "grasps": {
#             0: "ngrasps",
#         },
#         "confidence": {
#             0: "ngrasps",
#         },
#     }
#     model.eval()
#     wrapped_cgn = WrappedCGN(model)
#     wrapped_cgn.eval()
#     dummy_input = torch.randn(20000, 3)
#     torch.onnx.export(
#         wrapped_cgn,
#         dummy_input,
#         save_path,
#         verbose=False,
#         input_names=["input"],
#         output_names=["grasps", "confidence"],
#         dynamic_axes=dynamic_axes_dict,
#         export_params=True,
#     )
