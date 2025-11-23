from collections import deque

def neighbours(node):
    r, c = node
    return [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]

def is_free(grid, r, c):
    return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1] and grid[r, c] == 0

def bfs(start, goal, grid):
    q = deque([start])
    parents = {start: None}
    visited = set([start])
    expanded = 0

    while q:
        cur = q.popleft()
        expanded += 1  # count expansion when you pop/process a node

        if cur == goal:
            # reconstruct path
            path = []
            while cur is not None:
                path.append(cur)
                cur = parents[cur]
            path.reverse()
            cost = len(path) - 1
            return path, expanded, cost

        r, c = cur
        for nr, nc in neighbours(cur):
            if is_free(grid, nr, nc) and (nr, nc) not in visited:
                visited.add((nr, nc))
                parents[(nr, nc)] = cur
                q.append((nr, nc))

    return [], expanded, None
