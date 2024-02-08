import random

def generate_maze(width, height):
    print(f"Generating maze with dimensions: {width}x{height}")
    # Initialize the maze grid with walls (1s)
    maze = [[1 for _ in range(width)] for _ in range(height)]
    
    # Define start position, traditionally at the top-left corner for simplicity
    start_x, start_y = (1, 1)
    maze[start_y][start_x] = 0  # Set the start position to path
    print(f"Start position set at: ({start_x}, {start_y})")

    # Steps to move in the cardinal directions
    directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]

    def carve_path(x, y):
        # Randomize the directions to ensure a random maze
        random.shuffle(directions)

        # Explore each direction
        for dx, dy in directions:
            nx, ny = x + dx, y + dy  # New position after moving

            # Check if the new position is within the maze bounds
            if (0 < nx < width-1) and (0 < ny < height-1) and (maze[ny][nx] == 1):
                # Carve a path to the new cell and the cell in between
                maze[ny][nx] = 0
                maze[ny - dy // 2][nx - dx // 2] = 0
                carve_path(nx, ny)

    # Start carving the maze from the initial position
    carve_path(start_x, start_y)

    # Optionally, create an exit by setting a position at the opposite corner to path
    end_x, end_y = (width - 2, height - 2)
    maze[end_y][end_x] = 0
    print(f"End position set at: ({end_x}, {end_y})")

    # Print the generated maze to console
    print("Generated maze:")
    for row in maze:
        print(''.join(['#' if cell == 1 else ' ' for cell in row]))
    
    return maze, (start_x, start_y), (end_x, end_y)

# Example usage:
if __name__ == "__main__":
    width, height = 21, 21  # Maze dimensions (must be odd numbers)
    maze, start, end = generate_maze(width, height)
