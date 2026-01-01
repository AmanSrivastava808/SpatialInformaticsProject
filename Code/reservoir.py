import os
import glob
import rasterio
import geopandas as gpd
import numpy as np
from shapely.geometry import box
import pandas as pd
import matplotlib.pyplot as plt

CHIRPS_FOLDER = "CHIRPS/"
RESERVOIR_FOLDER = "Reservoirs2/"

# Detect season
def extract_info(filename):
    name = os.path.basename(filename)
    parts = name.split("_")

    season_raw = parts[1].lower()
    if "winter" in season_raw:
        season = "Winter"
        season_code = "01_Winter"
    elif "summer" in season_raw:
        season = "Summer"
        season_code = "02_Summer"
    elif "monsoon" in season_raw:
        season = "Monsoon"
        season_code = "03_Monsoon"
    else:
        raise ValueError(f"Cannot detect season from: {name}")

    year = int(parts[2].split(".")[0])
    return year, season, season_code


results = []

# Process CHIRPS files
chirps_files = sorted(glob.glob(os.path.join(CHIRPS_FOLDER, "*.tif")))

for chirps_file in chirps_files:
    year, season, season_code = extract_info(chirps_file)
    print(f"\nProcessing Reservoir vs Rainfall → {season} {year}")

    # Load CHIRPS raster
    with rasterio.open(chirps_file) as src:
        chirps = src.read(1).astype("float32")
        rainfall_mean = float(np.nanmean(chirps))
        raster_crs = src.crs
        bounds = src.bounds

    # Matching reservoir file
    res_file = os.path.join(
        RESERVOIR_FOLDER,
        f"reservoirs_{year}_{season_code}_NDWI_MNDWI_WATERMASK.shp"
    )

    if not os.path.exists(res_file):
        print(f"  ❌ Reservoir file missing: {res_file}")
        results.append([year, season, rainfall_mean, np.nan])
        continue

    # Load reservoir shapefile
    reservoir = gpd.read_file(res_file).to_crs(raster_crs)

    if reservoir.empty:
        print("  ❌ Reservoir shapefile empty.")
        results.append([year, season, rainfall_mean, np.nan])
        continue

    # Calculate reservoir area
    reservoir_geom = reservoir.unary_union
    area_m2 = reservoir_geom.area
    area_km2 = float(area_m2) / 1e6

    results.append([year, season, rainfall_mean, area_km2])

# Convert to DataFrame
df = pd.DataFrame(results, columns=[
    "Year", "Season", "Rainfall_mm", "ReservoirArea_km2"
])

df = df.sort_values(["Season", "Year"])
df.to_csv("Reservoir_vs_Rainfall.csv", index=False)
print("\n✔ Saved → Reservoir_vs_Rainfall.csv")

# ---------------------------------------------------------
# PLOTS
# ---------------------------------------------------------

# 1) Reservoir Area Trend
plt.figure(figsize=(8,5))
plt.plot(df["Year"], df["ReservoirArea_km2"], marker="o")
plt.title("Reservoir Area Trend Over Years")
plt.xlabel("Year")
plt.ylabel("Reservoir Area (km²)")
plt.grid(True)
plt.show()

# 2) Rainfall Trend
plt.figure(figsize=(8,5))
plt.plot(df["Year"], df["Rainfall_mm"], marker="o", color="green")
plt.title("Rainfall Trend Over Years (CHIRPS)")
plt.xlabel("Year")
plt.ylabel("Rainfall (mm)")
plt.grid(True)
plt.show()

# 3) Rainfall vs Reservoir Area
plt.figure(figsize=(8,5))
plt.scatter(df["Rainfall_mm"], df["ReservoirArea_km2"], s=80)
plt.title("Rainfall vs Reservoir Area")
plt.xlabel("Rainfall (mm)")
plt.ylabel("Reservoir Area (km²)")
plt.grid(True)
plt.show()

# 4) Seasonal comparison
seasons = df["Season"].unique()
for season in seasons:
    sdata = df[df["Season"] == season]

    plt.figure(figsize=(8,5))
    plt.plot(sdata["Year"], sdata["ReservoirArea_km2"], marker="o")
    plt.title(f"{season}: Reservoir Area Trend")
    plt.xlabel("Year")
    plt.ylabel("Reservoir Area (km²)")
    plt.grid(True)
    plt.show()

print("\n🎉 All reservoir analysis completed successfully!")
