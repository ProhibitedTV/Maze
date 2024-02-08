import pygame
from OpenGL.GL import *
from renderer import Renderer
from maze_generator import generate_maze
from camera import Camera
from pathfinding import find_path

def lerp(start, end, t):
    """Linearly interpolate between start and end points."""
    return start + t * (end - start)

def restart_maze():
    # Assuming generate_maze returns a maze and start/end points
    maze, start, end = generate_maze(21, 21)  # Adjust dimensions as necessary
    path = find_path(start, end, maze)  # Calculate a path through the maze
    return maze, path, 0  # Return the maze, the calculated path, and reset the path index to 0

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF|pygame.OPENGL)
    pygame.display.set_caption('3D Maze Screensaver')

    glEnable(GL_DEPTH_TEST)

    camera = Camera()
    renderer = Renderer(camera)
    
    maze, path, path_index = restart_maze()  # Initialize the maze and path

    # Initialize interpolation variables
    t = 0.0
    interpolation_speed = 0.05  # Adjust as needed for smoother movement
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if path and path_index < len(path) - 1:
            current_point = path[path_index]
            next_point = path[path_index + 1]
            camera.position[0] = lerp(current_point[0], next_point[0], t)  # X-axis
            camera.position[2] = lerp(current_point[1], next_point[1], t)  # Z-axis (assuming Y is up)
            t += interpolation_speed
            if t >= 1.0:
                t = 0.0
                path_index += 1
        else:
            maze, path, path_index = restart_maze()  # Reset when reaching the end
            t = 0.0

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        renderer.render(maze)

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
