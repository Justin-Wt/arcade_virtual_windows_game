from collections import deque

grid = [
    [0, 0, 0, 1, 0],
    [1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
]

start = (0, 0)
goal = (4, 4)

queue = deque([(start, [])])
visited = set()

directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

while queue:
    (x, y), path = queue.popleft()

    if (x, y) in visited:
        continue

    visited.add((x, y))

    path = path + [(x, y)]

    if (x, y) == goal:
        print("Path found:", path)
        break

    for dx, dy in directions:
        nx = x + dx
        ny = y + dy

        if 0 <= nx < 5 and 0 <= ny < 5:
            if grid[ny][nx] == 0:
                queue.append(((nx, ny), path))
