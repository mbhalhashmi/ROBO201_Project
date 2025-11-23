#!/usr/bin/env python3

import os
import time
import numpy as np
import matplotlib.pyplot as plt

#Importing Path Planning Algorithims and SLAM convertor

from read_map import load_grid_from_yaml
from bfs import bfs
from dijkstra import dijkstra
from Astar import astar

def run_experiments():
    #Load Map

    project_dir=os.path.dirname(os.path.dirname(__file__))
    yaml_path = os.path.join(os.path.dirname(project_dir), "maps", "my_robot_map_real.yaml")

    #Load occupancy grid using the map loader
    grid, res, img_path = load_grid_from_yaml(yaml_path)

    #Print map info to ensure it works
    print(f"Map loaded: {yaml_path}")
    print(f"Grid Shape: {grid.shape}, Resolution: {res} m/cell")
    print(f"Unique values in grid: {np.unique(grid)}")

    # Define Start and Goal

    start=(32,15)
    goal=(65, 36)

   
    # Run all algorithims

    algorithims= {
        "BFS": bfs,
        "Dijkstra": dijkstra,
        "A*": astar
    }

    results = {} #Dictionary to store results

    # Loop through each algorithim, run it, and measure it's performance

    for name, func in algorithims.items():
        print(f"\n Running {name}...")
        t0 = time.time()
        out = func(start, goal, grid)   # different algos may return different shapes
        dt = time.time() - t0

        # Accept either: path-only  OR  (path, expanded, cost)
        if isinstance(out, tuple) and len(out) == 3:
            path, expanded, cost = out
        else:
            path = out
            expanded = None
            cost = len(path) - 1 if path else None

        results[name] = {"path": path, "time": dt, "cost": cost, "expanded": expanded}
        print(f"{name}: time={dt:.3f}s | cost={cost} | expanded={expanded}")

        
    # Plotting the results
    plt.figure(figsize=(15, 5))

    # Create one subplot per algorithim
    for i, (algo, data) in enumerate(results.items()):
        plt.subplot(1, 3, i + 1)

        #Plot the occupancy grid
        # (1 - grid) to flip the colors
        plt.imshow(1 - grid, cmap="gray", origin="upper")

        # Plot the path in blue
        if data["path"]:
            xs = [c for (r, c) in data["path"]]
            ys = [r for (r, c) in data["path"]]
            plt.plot(xs, ys, color="blue", linewidth=1.8)
        # Mark start as red and goal as green
        plt.scatter(start[1], start[0], color="red", s=50, label="Start")
        plt.scatter(goal[1], goal[0], color="green", s=50, label="Goal")

        exp_str = f" | Nodes={data['expanded']}" if data['expanded'] is not None else ""
        # Add title showing the time and cost
            
        plt.title(f"{algo}\nTime={data['time']:.3f}s | Cost={data['cost']}{exp_str}")
        plt.axis("off")

    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__== "__main__":
    run_experiments()