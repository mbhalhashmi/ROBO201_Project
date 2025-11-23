from queue import PriorityQueue

def neighbours(node):
    r, c = node
    return [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]

def is_free(grid, r, c):
    return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1] and grid[r, c] == 0

def dijkstra(start, goal, grid):
    open_list = PriorityQueue()
    open_list.put((0, start))
    visited = set()
    parents = {start: None}
    g = {start: 0}
    expanded = 0

    while not open_list.empty():
        cost, cur = open_list.get()
        if cur in visited:
            continue
        visited.add(cur)
        expanded += 1  # expansion when we settle a node

        if cur == goal:
            # reconstruct
            path = []
            while cur is not None:
                path.append(cur)
                cur = parents[cur]
            path.reverse()
            return path, expanded, cost

        r, c = cur
        for nr, nc in neighbours(cur):
            if is_free(grid, nr, nc):
                nxt = (nr, nc)
                new_cost = cost + 1
                if new_cost < g.get(nxt, float('inf')):
                    g[nxt] = new_cost
                    parents[nxt] = (r, c)
                    open_list.put((new_cost, nxt))

    return [], expanded, None
