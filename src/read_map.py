
import os
import yaml
import numpy as np
import matplotlib.image as mpimg
import math

def inflate_obstacles(grid, radius_m, resolution):
    """grid: 0=free, 1=occ, -1=unknown. 
    Every occupied or unkown cell grows by a square neighborhood of 'r_cells'"""

    #If robot radius is 0 , skip inflation

    if radius_m <= 0:
        return grid

    #Convert robot radius to grid cells
    r_cells = int(math.ceil(radius_m / max(resolution, 1e-9)))
    if r_cells <= 0:
        return grid

    # Get grid dimensions
    h, w = grid.shape

    #Create a mask of all occupied and unkonwn cells
    occ_mask = (grid == 1) | (grid == -1)  # treat unknown as solid

    # Create a copy of the mask to modify as we inflate
    inflated = occ_mask.copy()

    #to get the coords of all obstaces cells
    coords = np.argwhere(occ_mask)

    # for each obstacle , mark a square region around it as occupied
    for r, c in coords:
        r0 = max(0, r - r_cells); r1 = min(h, r + r_cells + 1)
        c0 = max(0, c - r_cells); c1 = min(w, c + r_cells + 1)
        inflated[r0:r1, c0:c1] = True #Fill neighborhood

    # apply the inflated mask to the grid
    out = grid.copy()
    out[inflated] = 1 #Mark all inflated regions as occupied

    return out

def load_grid_from_yaml(yaml_path):
    """
    Reada the SLAM map's YAML file and the image file
    to create a 2D occupancy grid, and inflate the obstacles based on the robot's radius
    """

    # Load metadata from YAML
    with open(yaml_path, "r") as f:
        meta = yaml.safe_load(f)

    #Extract parameters from YAML

    image_path  = os.path.join(os.path.dirname(yaml_path), meta["image"])
    resolution  = float(meta["resolution"])
    occ_t       = float(meta["occupied_thresh"])
    free_t      = float(meta["free_thresh"])
    negate      = int(meta.get("negate", 0))

    # Load the map image

    img = mpimg.imread(image_path).astype(float)

    # Normalize image to [0,1] range if needed
    if img.max() > 1.0:
        img = img / 255.0

    # Convert pixel values to occupancy probabilites
    # negate=0: black(0) -> 1.0 (occupied), white(1) -> 0.0 (free)
    if negate == 0:
        occ_prob = 1.0 - img
    else:
        occ_prob = img

    #Flip vertically to match standard viewing orientation
    grid = np.full(img.shape, -1, dtype=np.int32) #start all as unknown
    grid[occ_prob >= occ_t] = 1      # occupied
    grid[occ_prob <= free_t] = 0      # free

    # Flip vertically to match usual viewing
    grid = np.flipud(grid)

    # Inflate obstacles
    robot_radius_m = 0.10
    grid = inflate_obstacles(grid, robot_radius_m, resolution)

    return grid, resolution, image_path


def main():

    share_dir = get_package_share_directory('slam_to_grid')
    yaml_path = os.path.join(share_dir, 'maps', 'my_robot_map_real.yaml')

    if not os.path.isfile(yaml_path):
        raise FileNotFoundError(
            f"Map YAML not found at:\n  {yaml_path}\n"
            "Did you install the maps in setup.py and rebuild?"
        )

    # load grid
    grid, res, img_path = load_grid_from_yaml(yaml_path)

    # Console summary
    print("Map loaded ")
    print(f" YAML path     : {yaml_path}")
    print(f" Image path    : {img_path}")
    print(f" Grid shape    : {grid.shape[0]} rows x {grid.shape[1]} cols")
    print(f" Resolution    : {res} m/cell")
    print(f" Unique values : {np.unique(grid)} (expected [-1, 0, 1])")

    # Visualization
    plt.imshow(1 - grid, cmap="gray", origin="upper")
    plt.title(f"Occupancy Grid (1=occ, 0=free, -1=unk)   res={res} m/cell")
    plt.xlabel("X →")
    plt.ylabel("Y →")
    plt.colorbar(label="Cell value")
    plt.show()

if __name__ == "__main__":
    main()
