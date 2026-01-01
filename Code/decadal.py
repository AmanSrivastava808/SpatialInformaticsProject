import rasterio
import numpy as np
import pandas as pd
import glob
import os
from math import cos, pi

# -------------------------------------------------------------
# FUNCTION: Compute area using latitude-aware pixel size
# -------------------------------------------------------------
def compute_reservoir_area(raster_path, water_value=1):
    with rasterio.open(raster_path) as src:
        arr = src.read(1)
        
        # Get bounds + CRS
        bounds = src.bounds
        width = src.width
        height = src.height

    # Convert degrees → metres using earth radius (lat-dependent)
    # 1 degree latitude = constant 111.32 km
    # 1 degree longitude = 111.32 * cos(latitude) km

    lat_center = (bounds.top + bounds.bottom) / 2

    pixel_width_deg  = (bounds.right - bounds.left) / width
    pixel_height_deg = (bounds.top - bounds.bottom) / height

    pixel_width_km  = 111.32 * cos(lat_center * pi / 180) * pixel_width_deg
    pixel_height_km = 111.32 * pixel_height_deg

    pixel_area_km2 = pixel_width_km * pixel_height_km

    # Count reservoir pixels
    water_pixels = np.sum(arr == water_value)

    # Compute area
    total_area_km2 = water_pixels * pixel_area_km2

    return total_area_km2


# -------------------------------------------------------------
# MAIN LOOP
# -------------------------------------------------------------
raster_folder = "mndwi/"
rasters = sorted(glob.glob(os.path.join(raster_folder, "*.tif")))

results = []

for r in rasters:
    year = os.path.basename(r).split(".")[0]
    print(f"Processing {year} ...")

    area = compute_reservoir_area(r, water_value=1)
    results.append((year, area))

df = pd.DataFrame(results, columns=["Year", "Reservoir_Area_km2"])

print(df)
df.to_csv("Reservoir_Area_Final.csv", index=False)
