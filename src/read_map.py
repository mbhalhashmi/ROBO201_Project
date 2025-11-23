
import os
import yaml
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def load_grid_from_yaml(yaml_path: str):
    """
    Read the map YAML + image and return (grid, resolution, image_path).

    1 = occupied
    0 = free
    -1 = unknown
    """

    # 1) Read YAML metadata
    with open(yaml_path, "r") as f:
        meta = yaml.safe_load(f)

    # Image path resolved relative to the YAML file
    image_path = os.path.join(os.path.dirname(yaml_path), meta["image"])

    resolution = float(meta["resolution"])
    occ_t = float(meta["occupied_thresh"])
    free_t = float(meta["free_thresh"])
    negate = int(meta.get("negate", 0))

    # 2) Load grayscale image (PGM/PNG). mpimg handles PGM fine.
    gray = mpimg.imread(image_path).astype(float)

    # Normalize to [0,1] if needed (some loaders return 0..255)
    if gray.max() > 1.0:
        gray = gray / 255.0

    # Optional inversion based on YAML flag
    if negate == 1:
        gray = 1.0 - gray

    # 3) Threshold into occupancy grid
    grid = np.full(gray.shape, -1, dtype=int)  # start as unknown
    grid[gray >= occ_t] = 1                    # occupied
    grid[gray <= free_t] = 0                   # free

    # 4) Flip vertically to match typical RViz / map orientation
    grid = np.flipud(grid)

    def inflate_obstacles(grid, radius_m, resolution):
        import math, numpy as np
        r_cells = int(math.ceil(radius_m / resolution))
        if r_cells <= 0:
            return grid
        h, w = grid.shape
        occ_mask = (grid == 1) | (grid == -1)  # treat unknown as obstacle
        inflated = occ_mask.copy()
        occ_coords = np.argwhere(occ_mask)
        for r, c in occ_coords:
            r0, r1 = max(0, r - r_cells), min(h, r + r_cells + 1)
            c0, c1 = max(0, c - r_cells), min(w, c + r_cells + 1)
            inflated[r0:r1, c0:c1] = True
        grid[inflated] = 1
        return grid

    # ---- inside load_grid_from_yaml ----
    robot_radius = 0.10  # meters
    grid = inflate_obstacles(grid, robot_radius, resolution)


    return grid, resolution, image_path

def main():
    # <pkg>/slam_to_grid/maps/my_robot_map_real.yaml
    # Use the installed share directory, not the build tree
    share_dir = get_package_share_directory('slam_to_grid')
    yaml_path = os.path.join(share_dir, 'maps', 'my_robot_map_real.yaml')

    if not os.path.isfile(yaml_path):
        raise FileNotFoundError(
            f"Map YAML not found at:\n  {yaml_path}\n"
            "Did you install the maps in setup.py and rebuild?"
        )

    grid, res, img_path = load_grid_from_yaml(yaml_path)

    # Console summary
    print("Map loaded ")
    print(f" YAML path     : {yaml_path}")
    print(f" Image path    : {img_path}")
    print(f" Grid shape    : {grid.shape[0]} rows x {grid.shape[1]} cols")
    print(f" Resolution    : {res} m/cell")
    print(f" Unique values : {np.unique(grid)} (expected [-1, 0, 1])")

    # Visualization
    plt.imshow(grid, cmap="gray", origin="upper")
    plt.title(f"Occupancy Grid (1=occ, 0=free, -1=unk)   res={res} m/cell")
    plt.xlabel("X →")
    plt.ylabel("Y →")
    plt.colorbar(label="Cell value")
    plt.show()

if __name__ == "__main__":
    main()
