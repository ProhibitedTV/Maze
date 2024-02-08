import heapq

def heuristic(a, b):
    """Calculate the Manhattan distance between two points."""
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

def find_neighbors(maze, current):
    """Find walkable neighbor cells of the current cell."""
    neighbors = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Down, Right, Up, Left
    for dx, dy in directions:
        nx, ny = current[0] + dx, current[1] + dy

        # Ensure nx and ny are within the bounds of the maze
        if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze):
            if maze[ny][nx] == 0:  # Check if the cell is a path (not a wall)
                neighbors.append((nx, ny))
    return neighbors

def find_path(start, end, maze):
    """Find a path from start to end in the maze using the A* algorithm."""
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    print(f"Maze dimensions: Height={len(maze)}, Width={len(maze[0])}")

    while not len(frontier) == 0:
        current = heapq.heappop(frontier)[1]

        if current == end:
            break

        for next in find_neighbors(maze, current):
            new_cost = cost_so_far[current] + 1  # Assumes the cost between neighboring cells is 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(end, next)
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current

    # Check if a path was successfully found
    if end not in came_from:
        print("No path found from start to end.")
        return []

    # Reconstruct the path from end to start
    path = []
    current = end
    while current != start:  # This assumes a path exists; handled by the check above
        path.append(current)
        current = came_from.get(current, start)  # Fallback to start to prevent infinite loop
    path.append(start)  # Add the start position
    path.reverse()  # Reverse the path to start --> end
    return path
