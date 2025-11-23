from queue import PriorityQueue

# returns 4 connected neighbors
def neighbours(node):
    r, c = node
    return [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]

# checks if a given cell is within bounds
def is_free(grid, r, c):
    return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1] and grid[r, c] == 0


def dijkstra(start, goal, grid):
    # Priority queue ensures the lowest cost node is expanded
    open_list = PriorityQueue()
    open_list.put((0, start)) #cost, node

    visited = set() # stores nodes already processed
    parents = {start: None} # for reconstuction of the path
    g = {start: 0} # g(n): cost from start node to n
    expanded = 0 # counter for node expansions

    # Main loop
    while not open_list.empty():
        cost, cur = open_list.get() # pop the node with smallest cost

        # skip nodes we've visited
        if cur in visited:
            continue
        visited.add(cur)
        expanded += 1  # expansion when we settle a node

        # goal test
        if cur == goal:
            # reconstruct
            path = []
            while cur is not None:
                path.append(cur)
                cur = parents[cur]
            path.reverse()
            return path, expanded, cost

        # otherwise explore the nieghbors
        r, c = cur
        for nr, nc in neighbours(cur):
            if is_free(grid, nr, nc): # check free and within bounds
                nxt = (nr, nc)
                new_cost = cost + 1 # step cost

                # update if this path is cheaper
                if new_cost < g.get(nxt, float('inf')):
                    g[nxt] = new_cost
                    parents[nxt] = (r, c)
                    open_list.put((new_cost, nxt)) # push neighbor to queue

    # if the open list is empty no path was found
    return [], expanded, None
