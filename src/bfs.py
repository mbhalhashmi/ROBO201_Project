from collections import deque

def is_valid(node, grid):
    r, c = node
    rows, cols = grid.shape
    return 0 <= r < rows and 0 <= c < cols and grid[r][c] == 0

def neighbours(node):
    r, c = node
    return [
        (r-1, c),
        (r+1, c),
        (r, c-1),
        (r, c+1)
    ]

def bfs(start, goal, grid):
    queue = deque([start])
    visited = set([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        for nxt in neighbours(current):
            if is_valid(nxt, grid) and nxt not in visited:
                visited.add(nxt)
                parent[nxt] = current
                queue.append(nxt)

    # reconstruct path
    if goal not in parent:
        print("No path found")
        return []

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]

    return path[::-1]
