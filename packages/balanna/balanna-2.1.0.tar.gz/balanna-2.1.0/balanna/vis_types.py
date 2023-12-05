import numpy as np
import trimesh
import trimesh.creation

from balanna.trimesh import show_point_cloud, show_trajectory
from dataclasses import dataclass
from typing import Tuple


class VisType:

    def transform(self, T: np.ndarray) -> 'VisType':
        raise NotImplementedError

    def add_to_scene(self, scene: trimesh.Scene) -> trimesh.Scene:
        raise NotImplementedError


@dataclass(frozen=True)
class PointCloudWColors(VisType):
    points: np.ndarray  # (N, 3)
    colors: np.ndarray  # (N, 3), [0, 1] range

    def __post_init__(self):
        if not isinstance(self.points, np.ndarray) or not isinstance(self.colors, np.ndarray):
            raise ValueError(f"Expected points and colors to be numpy arrays, got {type(self.points)} and {type(self.colors)}")
        if self.points.ndim != 2 or self.points.shape[1] != 3:
            raise ValueError(f"Expected 3D points to have shape (N, 3), got {self.points.shape}")
        if self.colors.ndim != 2 or self.colors.shape[1] != 3:
            raise ValueError(f"Expected RGB colors to have shape (N, 3), got {self.colors.shape}")
        if self.points.shape[0] != self.colors.shape[0]:
            raise ValueError(f"Expected points and colors to have the same number of points, got {self.points.shape[0]} and {self.colors.shape[0]}")
        if self.colors.dtype not in [np.float32, np.float64]:
            raise ValueError(f"Expected colors to be float, got {self.colors.dtype}")

    @classmethod
    def from_uniform_color(cls, points: np.ndarray, color: np.ndarray):
        if color.shape != (3,):
            raise ValueError(f"Expected RGB color of shape (3,), got {color.shape}")
        if points.ndim != 2 or points.shape[1] != 3:
            raise ValueError(f"Expected points to have shape (N, 3), got {points.shape}")
        colors = np.repeat(color[None, :], points.shape[0], axis=0)
        return cls(points, colors)

    def transform(self, T: np.ndarray) -> 'PointCloudWColors':
        if T.shape != (4, 4):
            raise ValueError(f"Expected transformation matrix to have shape (4, 4), got {T.shape}")
        points_tf = np.matmul(T[:3, :3], self.points.T).T + T[:3, 3]
        return PointCloudWColors(points_tf, self.colors)

    def add_to_scene(self, scene: trimesh.Scene) -> trimesh.Scene:
        return show_point_cloud(self.points, colors=self.colors, scene=scene)


@dataclass(frozen=True)
class Sphere(VisType):
    point: np.ndarray  # (3,)
    radius: float
    color: np.ndarray  # (3,)

    def __post_init__(self):
        if not isinstance(self.point, np.ndarray) or not isinstance(self.color, np.ndarray):
            raise ValueError(f"Expected point and color to be numpy arrays, got {type(self.point)} and {type(self.color)}")
        if self.point.shape != (3,):
            raise ValueError(f"Expected 3D point to have shape (3,), got {self.point.shape}")
        if self.color.shape != (3,) or self.color.dtype not in [np.float32, np.float64]:
            raise ValueError(f"Expected RGB color to have shape (3,), got {self.color.shape}, and type float, got {self.color.dtype}")
        if self.radius <= 0:
            raise ValueError(f"Expected radius to be positive, got {self.radius}")

    def transform(self, T: np.ndarray) -> 'Sphere':
        if T.shape != (4, 4):
            raise ValueError(f"Expected transformation matrix to have shape (4, 4), got {T.shape}")
        point_tf = np.matmul(T[:3, :3], self.point) + T[:3, 3]
        return Sphere(point_tf, self.radius, self.color)

    def add_to_scene(self, scene: trimesh.Scene) -> trimesh.Scene:
        if self.radius < 0.01:
            return scene  # skip adding spheres that are too small

        sphere = trimesh.creation.uv_sphere(radius=self.radius)
        color_uint8 = (self.color * 255).astype(np.uint8)
        sphere.visual.face_colors = np.repeat(color_uint8[None, :], len(sphere.faces), axis=0)
        sphere.apply_translation(self.point)

        scene.add_geometry(sphere)
        return scene


@dataclass(frozen=True)
class Capsule(VisType):
    point_1: np.ndarray  # (3,)
    points_2: np.ndarray  # (3,)
    radius: float
    color: np.ndarray  # (3,)

    def __post_init__(self):
        if not isinstance(self.point_1, np.ndarray) or not isinstance(self.points_2, np.ndarray) or not isinstance(self.color, np.ndarray):
            raise ValueError(f"Expected p1, p2 and color to be numpy arrays, got {type(self.point_1)}, {type(self.points_2)} and {type(self.color)}")
        if self.point_1.shape != (3,):
            raise ValueError(f"Expected 3D point to have shape (3,), got {self.point_1.shape}")
        if self.points_2.shape != (3,):
            raise ValueError(f"Expected 3D point to have shape (3,), got {self.points_2.shape}")
        if self.radius <= 0:
            raise ValueError(f"Expected radius to be positive, got {self.radius}")
        if self.color.shape != (3,) or self.color.dtype not in [np.float32, np.float64]:
            raise ValueError(f"Expected RGB color to have shape (3,), got {self.color.shape}, and type float, got {self.color.dtype}")

    def transform(self, T: np.ndarray) -> 'Capsule':
        if T.shape != (4, 4):
            raise ValueError(f"Expected transformation matrix to have shape (4, 4), got {T.shape}")
        p1_tf = np.matmul(T[:3, :3], self.point_1) + T[:3, 3]
        p2_tf = np.matmul(T[:3, :3], self.points_2) + T[:3, 3]
        return Capsule(p1_tf, p2_tf, self.radius, self.color)

    def add_to_scene(self, scene: trimesh.Scene) -> trimesh.Scene:
        center, height, radius, Rc = self.compute_canonical_representation()
        Tz = np.eye(4)
        Tz[:3, 3] = center
        Tz[:3, :3] = Rc
        capsule_mesh = trimesh.creation.capsule(radius=self.radius, height=height, transform=Tz)
        scene.add_geometry(capsule_mesh)
        return scene

    def compute_canonical_representation(self) -> Tuple[np.ndarray, float, float, np.ndarray]:
        """The canonical capsule primitive is defined as a cylinder with its z-axis aligned with the world z-axis.
        It is determined by a single point P in the center of the cylinder and a height h. 
        
        This function computes the transformation from this canonical capsule to the capsule defined here from the 
        points p1 and p2. The canonical representation is given by:
        - The origin of the capsule (P = center).
        - The height of the capsule (h).
        - The radius of the capsule (r).
        - The orientation from the canonical representation (Rc).
        
        @return The canonical representation of the capsule, i.e. P, h, r, Rc.
        """
        dp = self.points_2 - self.point_1
        height = np.linalg.norm(dp)
        z_axis = np.array([0, 0, 1])
        dp_normed = dp / height

        # To compute the rotation matrix that rotates the z-axis to dp, we use the Rodrigues formula.
        # See https://math.stackexchange.com/questions/180418/calculate-rotation-matrix-to-align-vector-a-to-vector-b-in-3d
        v = np.cross(z_axis, dp_normed)
        s = np.linalg.norm(v)
        c = np.dot(z_axis, dp_normed)
        vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])  # skew-symmetric matrix of v

        Rc = np.eye(3) + vx + np.matmul(vx, vx) * (1 - c) / (s ** 2 + 1e-6)  # Rodrigues formula
        center = self.point_1 + dp / 2  # equals P
        return center, height, self.radius, Rc


@dataclass(frozen=True)
class Trajectory(VisType):
    points: np.ndarray  # (N >= 2, 3)
    color: np.ndarray  # (3,)

    def __post_init__(self):
        if not isinstance(self.points, np.ndarray) or not isinstance(self.color, np.ndarray):
            raise ValueError(f"Expected points and color to be numpy arrays, got {type(self.points)} and {type(self.color)}")
        if self.points.ndim != 2 or self.points.shape[1] != 3 or self.points.shape[0] < 2:
            raise ValueError(f"Expected trajectory points to have shape (N >= 2, 3), got {self.points.shape}")
        if self.color.shape != (3,) or self.color.dtype not in [np.float32, np.float64]:
            raise ValueError(f"Expected RGB color to have shape (3,), got {self.color.shape}, and type float, got {self.color.dtype}")

    def transform(self, T: np.ndarray) -> 'Trajectory':
        if T.shape != (4, 4):
            raise ValueError(f"Expected transformation matrix to have shape (4, 4), got {T.shape}")
        points_tf = np.matmul(T[:3, :3], self.points.T).T + T[:3, 3]
        return Trajectory(points_tf, self.color)

    def add_to_scene(self, scene: trimesh.Scene, fade_out: bool = False) -> trimesh.Scene:
        return show_trajectory(self.points, colors=tuple(self.color), fade_out=fade_out, scene=scene)
