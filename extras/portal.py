from core.mesh import Mesh
from core.matrix import Mat44
from core.camera import Camera
from core.Object3D import Object3D
from geometry import RectangleGeometry
from material.surface import SurfaceMaterial
import numpy as np

class Portal(Mesh):
    def __init__(self, width=1.5, height=2.5) -> None:
        super().__init__(RectangleGeometry(width, height), SurfaceMaterial({"baseColor": [1, 1, 1]}))
        self.translate(0, height/2, 0)
        self.add(Mesh(RectangleGeometry(width, height=0.1), SurfaceMaterial({"baseColor": [0, 0, 0]})).translate(0, (0.1+height)/2, 0.0001))
        self.add(Mesh(RectangleGeometry(width=height+0.1, height=0.1), SurfaceMaterial({"baseColor": [0, 0, 0]})).translate(-(0.1+width)/2, 0.05, 0.0001).rotate_z(np.pi/2))
        self.add(Mesh(RectangleGeometry(width=height+0.1, height=0.1), SurfaceMaterial({"baseColor": [0, 0, 0]})).translate((0.1+width)/2, 0.05, 0.0001).rotate_z(-np.pi/2))
        self.destination: Portal = None

    def check_teleport(self, object: Object3D):
        forward = -self.get_direction()
        m_normal = forward / np.linalg.norm(forward)
        m_distance = -np.dot(m_normal, self.get_world_position())
        portal_plane = np.array([*m_normal, m_distance])

        x, y, z = object.get_world_position()
        A, B, C, D = portal_plane

        distance = abs(A*x + B*y + C*z + D) / np.sqrt(A**2 + B**2 + C**2)

        if distance < 0.05:
            rotate_180 = Mat44.make_rotation_y(np.pi)
            relative_view = np.linalg.inv(self.get_world_matrix()) @ object.get_world_matrix()
            relative_view = rotate_180 @ relative_view
            destination_view = self.destination.get_world_matrix() @ relative_view
            object.set_position(destination_view[:3, 3])
            object.set_rotation(destination_view[:3, :3])
            object.update_view_matrix()


    def set_destination_view(self, player_cam: Camera, portal_cam: Camera) -> None:
        if self.destination is None:
            raise Exception('Portal does not have a destination portal yet.')

        rotate_180 = Mat44.make_rotation_y(np.pi)

        # 1. get position of player cam relative to the source portal by inverting the source portal's transformation back to origin
        relative_view = np.linalg.inv(self.get_world_matrix()) @ player_cam.get_world_matrix()
        # 2. rotate that transformation by 180 since we want the destination view to be looking out of the portal
        relative_view = rotate_180 @ relative_view
        # 3. now translate the view by the destination portal's tranformation matrix
        destination_view = self.destination.get_world_matrix() @ relative_view

        # 4. update transform of destination camera 
        portal_cam.set_position(destination_view[:3, 3])
        portal_cam.set_rotation(destination_view[:3, :3])
        portal_cam.update_view_matrix()

        # 5. oblique projection to clip the portal_cam near plane to the destination portal plane
        forward = -self.destination.get_direction()
        m_normal = forward / np.linalg.norm(forward)
        m_distance = -np.dot(m_normal, self.destination.get_world_position())
        clip_plane = np.array([*m_normal, m_distance])
        clip_plane = np.linalg.inv(portal_cam.view_matrix).transpose() @ clip_plane
        q = np.linalg.inv(player_cam.projection_matrix) @ np.array([np.sign(clip_plane[0]), np.sign(clip_plane[1]), 1, 1])
        c = clip_plane * (2 / np.dot(clip_plane, q))
        portal_cam.projection_matrix[2, :] = np.subtract(c, portal_cam.projection_matrix[3, :])
