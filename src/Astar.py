import matplotlib.pyplot as plt
import numpy as np
from queue import PriorityQueue

# Checks if a node is inside the grid boundaries
def is_valid_node(node, grid):
    row, col = node
    rows, cols = grid.shape
    if row >= 0 and row < rows:
        if col >= 0 and col < cols:
            if grid[row][col] == 0:  # free space
                return True
    return False


# Returns the 4 connected neighbors for a cell

def neighbours(node):
    row, col = node
    top_node = (row - 1, col)
    bottom_node = (row + 1, col)
    right_node = (row, col + 1)
    left_node = (row, col - 1)
    return [top_node, bottom_node, left_node, right_node]

# Estimates the remaning cost from a node to a goal 

def heuristic(node1, node2):
    # Manhattan distance heuristic
    return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])


def astar(start_node, goal_node, grid):
    #Priority queue stores tuples of (f, node)
    # f = g + h
    open_list = PriorityQueue()
    open_list.put((0, start_node))

    closed_list = set() #stores already visited nodes
    parents = {start_node: None} # parent pointers for path reconstruction
    cost_from_start_node = {start_node: 0} #cost from start to current node
    expanded = 0  # node expansion counter

    # Main A* loop
    while not open_list.empty():
        # Get node with the lowest f value
        current_cost, current_node = open_list.get()

        # Skip duplicate entries already processed
        if current_node in closed_list:
            continue

        # Count this node as expanded
        expanded += 1
        closed_list.add(current_node)

        # Goal check
        if current_node == goal_node:
            break

        # Explore neighbours
        for next_node in neighbours(current_node):
            if is_valid_node(next_node, grid) and next_node not in closed_list:
                new_cost = cost_from_start_node[current_node] + 1  # step cost = 1
                if next_node not in cost_from_start_node or new_cost < cost_from_start_node[next_node]:
                    cost_from_start_node[next_node] = new_cost
                    parents[next_node] = current_node
                    
                    # f = g + h
                    priority_cost = new_cost + heuristic(next_node, goal_node)
                    open_list.put((priority_cost, next_node))

    # Reconstruct path
    path = []
    current_node = goal_node

    # Backtract from goal to start using parent dictionary
    while current_node != start_node:
        if current_node is None:
            return [], expanded, None  # return expanded even if no path found
        path.append(current_node)
        current_node = parents.get(current_node)
    path.append(start_node)
    path.reverse() # reverse to get the path from start to goal

    cost = len(path) - 1
    return path, expanded, cost
