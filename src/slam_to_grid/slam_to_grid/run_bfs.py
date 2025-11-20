import os
import matplotlib.pyplot as plt
from slam_to_grid.read_map import load_grid_from_yaml
from slam_to_grid.bfs import bfs

def plot(grid, start, goal, path):
    plt.imshow(grid, cmap="gray", origin="upper")

    if path:
        xs = [c for (r, c) in path]
        ys = [r for (r, c) in path]
        plt.plot(xs, ys, color="blue", linewidth=2)

    plt.scatter(start[1], start[0], color="red", label="Start", s=80)
    plt.scatter(goal[1], goal[0], color="green", label="Goal", s=80)

    plt.legend()
    plt.title("BFS Path on SLAM Map")
    plt.show()

if __name__ == "__main__":
    pkg_dir = os.path.dirname(__file__)
    yaml_path = os.path.join(pkg_dir, "maps", "my_robot_map_real.yaml")

    grid, res, img_path = load_grid_from_yaml(yaml_path)

    print("Grid Loaded!")
    print("Shape:", grid.shape)
    print("Resolution:", res)

    # Pick free-space start/goal cells
    start = (100, 50)
    goal  = (250, 120)

    path = bfs(start, goal, grid)
    plot(grid, start, goal, path)
