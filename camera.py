import numpy as np

class Camera:
    def __init__(self):
        self.position = [0, 0, 0]
        self.look_at = [0, 0, -1]
        self.up = [0, 1, 0]
        self.fov = 45
        self.aspect_ratio = 800 / 600
        self.near_plane = 0.1
        self.far_plane = 50.0

    def get_projection_matrix(self):
        # Manually create a perspective projection matrix
        f = 1.0 / np.tan(np.radians(self.fov) / 2.0)
        aspect_ratio = self.aspect_ratio
        z_near, z_far = self.near_plane, self.far_plane
        return np.array([
            [f / aspect_ratio, 0.0, 0.0, 0.0],
            [0.0, f, 0.0, 0.0],
            [0.0, 0.0, (z_far + z_near) / (z_near - z_far), (2.0 * z_far * z_near) / (z_near - z_far)],
            [0.0, 0.0, -1.0, 0.0]
        ], dtype=np.float32)

    def get_view_matrix(self):
        # Create a view matrix based on the camera's position, look_at point, and up vector
        return gluLookAt(
            self.position[0], self.position[1], self.position[2],
            self.look_at[0], self.look_at[1], self.look_at[2],
            self.up[0], self.up[1], self.up[2]
        )

    def get_view_matrix_without_translation(self):
        return np.identity(4, dtype=np.float32)
