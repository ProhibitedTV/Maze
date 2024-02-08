import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from shaders import create_shader_program
import numpy as np

def load_texture(image_path):
    textureSurface = pygame.image.load(image_path)
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    textureID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textureID)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    return textureID

class Renderer:
    def __init__(self, camera):
        self.camera = camera
        self.wall_texture = load_texture("textures/bricks.png")
        self.skybox_texture = load_texture("textures/skybox.png")
        self.skybox_shader_program = self.load_skybox_shader_program()
        self.skybox_vao = self.setup_skybox_geometry()

    def load_skybox_shader_program(self):
        vertex_shader_path = 'shaders/skybox.vert'
        fragment_shader_path = 'shaders/skybox.frag'
        return create_shader_program(vertex_shader_path, fragment_shader_path)

    def setup_skybox_geometry(self):
        # Skybox vertices (a simple cube)
        skybox_vertices = np.array([
            -1.0,  1.0, -1.0,
            -1.0, -1.0, -1.0,
             1.0, -1.0, -1.0,
             1.0, -1.0, -1.0,
             1.0,  1.0, -1.0,
            -1.0,  1.0, -1.0,

            -1.0, -1.0,  1.0,
            -1.0, -1.0, -1.0,
            -1.0,  1.0, -1.0,
            -1.0,  1.0, -1.0,
            -1.0,  1.0,  1.0,
            -1.0, -1.0,  1.0,

             1.0, -1.0, -1.0,
             1.0, -1.0,  1.0,
             1.0,  1.0,  1.0,
             1.0,  1.0,  1.0,
             1.0,  1.0, -1.0,
             1.0, -1.0, -1.0,

            -1.0, -1.0,  1.0,
            -1.0,  1.0,  1.0,
             1.0,  1.0,  1.0,
             1.0,  1.0,  1.0,
             1.0, -1.0,  1.0,
            -1.0, -1.0,  1.0,

            -1.0,  1.0, -1.0,
             1.0,  1.0, -1.0,
             1.0,  1.0,  1.0,
             1.0,  1.0,  1.0,
            -1.0,  1.0,  1.0,
            -1.0,  1.0, -1.0,

            -1.0, -1.0, -1.0,
            -1.0, -1.0,  1.0,
             1.0, -1.0, -1.0,
             1.0, -1.0, -1.0,
            -1.0, -1.0,  1.0,
             1.0, -1.0,  1.0
        ], dtype=np.float32)

        # Create VAO and VBO
        vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)
        
        glBindVertexArray(vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, skybox_vertices.nbytes, skybox_vertices, GL_STATIC_DRAW)
        
        # Position attribute
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * skybox_vertices.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        
        return vao

    def render_skybox(self):
        glUseProgram(self.skybox_shader_program)
        glDepthMask(GL_FALSE)  # Disable depth write
        glBindVertexArray(self.skybox_vao)
        
        projection_location = glGetUniformLocation(self.skybox_shader_program, 'projection')
        view_location = glGetUniformLocation(self.skybox_shader_program, 'view')
        
        # Assuming get_projection_matrix() and get_view_matrix_without_translation() return numpy arrays
        glUniformMatrix4fv(projection_location, 1, GL_FALSE, self.camera.get_projection_matrix().flatten('F'))
        glUniformMatrix4fv(view_location, 1, GL_FALSE, self.camera.get_view_matrix_without_translation().flatten('F'))

        # Bind skybox texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.skybox_texture)
        
        glDrawArrays(GL_TRIANGLES, 0, 36)  # 6 faces * 2 triangles per face * 3 vertices per triangle
        glBindVertexArray(0)
        glDepthMask(GL_TRUE)  # Enable depth write
        
        glUseProgram(0)
        
    def setup_camera(self):
        """Setup the camera view."""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (800 / 600), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(
            self.camera.position[0], self.camera.position[1], self.camera.position[2],
            self.camera.look_at[0], self.camera.look_at[1], self.camera.look_at[2],
            0, 1, 0
        )

    def draw_textured_cube(self, position):
        """Draw a textured cube at the specified position."""
        glBindTexture(GL_TEXTURE_2D, self.wall_texture)

        glBegin(GL_QUADS)  # Start drawing quads
    
        # Front face
        glTexCoord2f(0, 0); glVertex3f(-0.5 + position[0], -0.5,  0.5 + position[2])
        glTexCoord2f(1, 0); glVertex3f( 0.5 + position[0], -0.5,  0.5 + position[2])
        glTexCoord2f(1, 1); glVertex3f( 0.5 + position[0],  0.5,  0.5 + position[2])
        glTexCoord2f(0, 1); glVertex3f(-0.5 + position[0],  0.5,  0.5 + position[2])

        # Back face
        glTexCoord2f(1, 0); glVertex3f(-0.5 + position[0], -0.5, -0.5 + position[2])
        glTexCoord2f(1, 1); glVertex3f(-0.5 + position[0],  0.5, -0.5 + position[2])
        glTexCoord2f(0, 1); glVertex3f( 0.5 + position[0],  0.5, -0.5 + position[2])
        glTexCoord2f(0, 0); glVertex3f( 0.5 + position[0], -0.5, -0.5 + position[2])

        # Top face
        glTexCoord2f(0, 1); glVertex3f(-0.5 + position[0],  0.5, -0.5 + position[2])
        glTexCoord2f(0, 0); glVertex3f(-0.5 + position[0],  0.5,  0.5 + position[2])
        glTexCoord2f(1, 0); glVertex3f( 0.5 + position[0],  0.5,  0.5 + position[2])
        glTexCoord2f(1, 1); glVertex3f( 0.5 + position[0],  0.5, -0.5 + position[2])

        # Bottom face
        glTexCoord2f(1, 1); glVertex3f(-0.5 + position[0], -0.5, -0.5 + position[2])
        glTexCoord2f(0, 1); glVertex3f( 0.5 + position[0], -0.5, -0.5 + position[2])
        glTexCoord2f(0, 0); glVertex3f( 0.5 + position[0], -0.5,  0.5 + position[2])
        glTexCoord2f(1, 0); glVertex3f(-0.5 + position[0], -0.5,  0.5 + position[2])

        # Right face
        glTexCoord2f(1, 0); glVertex3f( 0.5 + position[0], -0.5, -0.5 + position[2])
        glTexCoord2f(1, 1); glVertex3f( 0.5 + position[0],  0.5, -0.5 + position[2])
        glTexCoord2f(0, 1); glVertex3f( 0.5 + position[0],  0.5,  0.5 + position[2])
        glTexCoord2f(0, 0); glVertex3f( 0.5 + position[0], -0.5,  0.5 + position[2])

        # Left face
        glTexCoord2f(0, 0); glVertex3f(-0.5 + position[0], -0.5, -0.5 + position[2])
        glTexCoord2f(1, 0); glVertex3f(-0.5 + position[0], -0.5,  0.5 + position[2])
        glTexCoord2f(1, 1); glVertex3f(-0.5 + position[0],  0.5,  0.5 + position[2])
        glTexCoord2f(0, 1); glVertex3f(-0.5 + position[0],  0.5, -0.5 + position[2])

        glEnd()  # End drawing quads

    def render(self, maze):
        """Render the maze."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.setup_camera()
        self.render_skybox()
        glEnable(GL_TEXTURE_2D)  # Enable texturing
        
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == 1:  # If the cell is a wall, draw a textured cube
                    self.draw_textured_cube((x - len(row) // 2, 0, y - len(maze) // 2))
                    
        glDisable(GL_TEXTURE_2D)  # Disable texturing after drawing the maze
