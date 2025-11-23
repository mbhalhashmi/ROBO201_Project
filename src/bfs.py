from collections import deque

# Return the 4 connected neighbors
def neighbours(node):
    r, c = node
    return [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]

# Check if a cell (r, c) is within the grid and not an obstacle
def is_free(grid, r, c):
    return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1] and grid[r, c] == 0


def bfs(start, goal, grid):
    # initalize queue with the start node
    q = deque([start])

    # Diciotnary to track each node's parent to reconstruct path
    parents = {start: None}

    # Visited set to prevent re-exploring cells
    visited = set([start])
    
    #Counter for number of expanded nodes
    expanded = 0

    # Main BFS loop
    while q:
        # Pop the first element (FIFO queue)
        cur = q.popleft()
        expanded += 1  # count expansion when you pop/process a node

        # If goal is reached then reconstruct path and return
        if cur == goal:
            # reconstruct path
            path = []
            while cur is not None:
                path.append(cur)
                cur = parents[cur]
            path.reverse() # reverse to get path from start to goal
            cost = len(path) - 1
            return path, expanded, cost

        # otherwise explore valid neighbors
        r, c = cur
        for nr, nc in neighbours(cur):
            if is_free(grid, nr, nc) and (nr, nc) not in visited:
                visited.add((nr, nc)) #mark as visited
                parents[(nr, nc)] = cur #store parent
                q.append((nr, nc)) #enqueu neighbor

    # if queue is empty then no path found
    return [], expanded, None
