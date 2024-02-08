import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

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
        self.wall_texture = load_texture("textures/bricks.png")  # Load the wall texture

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
        glBegin(GL_QUADS)
        
        # Front face
        glTexCoord2f(0, 0); glVertex3f(-0.5 + position[0], -0.5 + position[1], 0.5 + position[2])
        glTexCoord2f(1, 0); glVertex3f(0.5 + position[0], -0.5 + position[1], 0.5 + position[2])
        glTexCoord2f(1, 1); glVertex3f(0.5 + position[0], 0.5 + position[1], 0.5 + position[2])
        glTexCoord2f(0, 1); glVertex3f(-0.5 + position[0], 0.5 + position[1], 0.5 + position[2])
        
        # Other faces (omitted for brevity) should also be defined here
        
        glEnd()

    def render(self, maze):
        """Render the maze."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.setup_camera()
        
        glEnable(GL_TEXTURE_2D)  # Enable texturing
        
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == 1:  # If the cell is a wall, draw a textured cube
                    self.draw_textured_cube((x - len(row) // 2, 0, y - len(maze) // 2))
                    
        glDisable(GL_TEXTURE_2D)  # Disable texturing after drawing the maze
