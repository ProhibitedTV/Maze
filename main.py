import pygame
from OpenGL.GL import *  # Ensure OpenGL functions are available
from renderer import Renderer
from maze_generator import generate_maze
from camera import Camera
from pathfinding import find_path

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF|pygame.OPENGL)
    pygame.display.set_caption('3D Maze Screensaver')

    glEnable(GL_DEPTH_TEST)  # Enable depth testing for correct rendering of 3D objects

    camera = Camera()
    renderer = Renderer(camera)

    # Function to start or restart the maze exploration
    def restart_maze():
        # Adjusted dimensions to match expected by pathfinding
        width, height = 21, 21  # Ensuring the maze is large enough
        maze, start, end = generate_maze(width, height)  # Correctly capturing returned start/end
        print(f"Generated maze dimensions: {len(maze)}x{len(maze[0])}")  # Debugging print
        path = find_path(start, end, maze)  # Calculate the path using the correct maze
        return maze, path, 0

    maze, path, path_index = restart_maze()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move the camera along the path
        if path_index < len(path):
            # Assuming your Camera's position attribute can be directly modified like this
            camera.position = [path[path_index][0], 0, path[path_index][1]]
            path_index += 1
        else:
            # Once the end is reached, generate a new maze and path
            maze, path, path_index = restart_maze()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  # Clear the screen and depth buffer
        renderer.render(maze)  # Render the maze

        pygame.display.flip()  # Update the display
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
