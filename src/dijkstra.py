from queue import PriorityQueue

def is_valid(node, grid):
    r, c = node
    rows, cols = grid.shape
    return (
        0 <= r < rows and
        0 <= c < cols and
        grid[r][c] == 0  # free cell
    )

def neighbours(node):
    r, c = node
    return [
        (r-1, c),
        (r+1, c),
        (r, c-1),
        (r, c+1)
    ]

def dijkstra(start, goal, grid):
    open_list = PriorityQueue()
    open_list.put((0, start))

    visited = set()
    parent = {start: None}
    cost = {start: 0}

    while not open_list.empty():
        curr_cost, curr = open_list.get()

        if curr == goal:
            break

        if curr in visited:
            continue
        visited.add(curr)

        for nxt in neighbours(curr):
            if is_valid(nxt, grid) and nxt not in visited:
                new_cost = curr_cost + 1
                if nxt not in cost or new_cost < cost[nxt]:
                    cost[nxt] = new_cost
                    parent[nxt] = curr
                    open_list.put((new_cost, nxt))

    # reconstruct path
    if goal not in parent:
        print("⚠️ No path found")
        return []

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]

    return path[::-1]
