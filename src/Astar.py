import matplotlib.pyplot as plt
import numpy as np
from queue import PriorityQueue

def is_valid_node(node, grid):
    row, col = node
    rows, cols = grid.shape
    if row >= 0 and row < rows:
        if col >= 0 and col < cols:
            if grid[row][col] == 0:  # free space
                return True
    return False


def neighbours(node):
    row, col = node
    top_node = (row - 1, col)
    bottom_node = (row + 1, col)
    right_node = (row, col + 1)
    left_node = (row, col - 1)
    return [top_node, bottom_node, left_node, right_node]


def heuristic(node1, node2):
    return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])  # Manhattan distance


def astar(start_node, goal_node, grid):
    open_list = PriorityQueue()
    open_list.put((0, start_node))
    closed_list = set()
    parents = {start_node: None}
    cost_from_start_node = {start_node: 0}

    while not open_list.empty():
        current_cost, current_node = open_list.get()

        if current_node == goal_node:
            break

        if current_node in closed_list:
            continue
        else:
            closed_list.add(current_node)

        for next_node in neighbours(current_node):
            if is_valid_node(next_node, grid) and next_node not in closed_list:
                new_cost = cost_from_start_node[current_node] + 1
                if next_node not in cost_from_start_node or new_cost < cost_from_start_node[next_node]:
                    cost_from_start_node[next_node] = new_cost
                    parents[next_node] = current_node
                    priority_cost = new_cost + heuristic(next_node, goal_node)
                    open_list.put((priority_cost, next_node))

    path = []
    current_node = goal_node
    while current_node != start_node:
        if current_node is None:
            return []
        path.append(current_node)
        current_node = parents.get(current_node)
    path.append(start_node)
    path.reverse()
    return path
