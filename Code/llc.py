import rasterio
import numpy as np
from sklearn.cluster import KMeans
from pathlib import Path

# -----------------------------------------------------------
# FOLDER PATHS
# -----------------------------------------------------------
input_dir = Path("bhuvan_lulc_annual_dec")      # folder with input RGB TIFFs
output_dir = Path("pct_outputs1")     # folder for PCT outputs
output_dir.mkdir(exist_ok=True)

NUM_COLORS = 12    # fixed palette size


# -----------------------------------------------------------
# STEP 1 — COLLECT RGB SAMPLES FROM ALL FILES
# -----------------------------------------------------------
print("📌 Collecting RGB samples from all images...")

all_samples = []

for tif in sorted(input_dir.glob("*.tif")):
    with rasterio.open(tif) as src:
        R = src.read(1).astype(np.float32)
        G = src.read(2).astype(np.float32)
        B = src.read(3).astype(np.float32)

    rgb = np.dstack((R, G, B)).reshape(-1, 3)

    mask = np.any(rgb != 0, axis=1)
    rgb_valid = rgb[mask]

    # limit sample size
    if rgb_valid.shape[0] > 200000:
        idx = np.random.choice(rgb_valid.shape[0], 200000, replace=False)
        rgb_valid = rgb_valid[idx]

    all_samples.append(rgb_valid)

all_samples = np.vstack(all_samples)
print(f"📦 Total collected RGB samples: {all_samples.shape[0]:,}")


# -----------------------------------------------------------
# STEP 2 — RUN GLOBAL KMEANS AND BUILD FIXED PALETTE
# -----------------------------------------------------------
print("\n🤖 Running GLOBAL KMeans to build fixed palette...")

kmeans_global = KMeans(n_clusters=NUM_COLORS, random_state=0, n_init=10)
kmeans_global.fit(all_samples)

PALETTE = kmeans_global.cluster_centers_.astype(np.uint8)

print("\n========= GLOBAL 12-COLOR PALETTE =========")
for i, (r, g, b) in enumerate(PALETTE):
    print(f"Index {i}: RGB({r},{g},{b}) → #{r:02X}{g:02X}{b:02X}")
print("===========================================\n")



# -----------------------------------------------------------
# STEP 3 — FUNCTION TO CONVERT USING GLOBAL PALETTE
# -----------------------------------------------------------
def convert_with_global_palette(input_path, output_path, palette):
    print(f"\nProcessing: {input_path.name}")

    with rasterio.open(input_path) as src:
        R = src.read(1)
        G = src.read(2)
        B = src.read(3)
        profile = src.profile

    rows, cols = R.shape
    rgb_data = np.dstack((R, G, B)).reshape(-1, 3).astype(np.float32)

    mask = np.any(rgb_data != 0, axis=1)
    rgb_valid = rgb_data[mask]

    # -------------------------------------------------------
    # TOLERANCE MATCHING (±1 RGB)
    # -------------------------------------------------------
    def find_tolerance_match(pixel):
        for idx, p in enumerate(palette):
            if (abs(pixel[0] - p[0]) <= 1 and
                abs(pixel[1] - p[1]) <= 1 and
                abs(pixel[2] - p[2]) <= 1):
                return idx
        return -1   # no hit → fallback to nearest

    tolerance_class = np.array([find_tolerance_match(px) for px in rgb_valid])

    # fallback mask
    need_fallback = (tolerance_class == -1)
    fallback_pixels = rgb_valid[need_fallback]

    # -------------------------------------------------------
    # Fallback to nearest palette color
    # -------------------------------------------------------
    if len(fallback_pixels) > 0:
        diff = fallback_pixels[:, None, :] - palette[None, :, :]
        dist = np.linalg.norm(diff, axis=2)
        nearest_idx = np.argmin(dist, axis=1)
        tolerance_class[need_fallback] = nearest_idx

    # final class mapping
    labels = np.full(rgb_data.shape[0], 0, dtype=np.uint8)
    labels[mask] = tolerance_class
    pct_raster = labels.reshape(rows, cols)

    # -------------------------------------------------------
    # Save output
    # -------------------------------------------------------
    profile.update({
        "count": 1,
        "dtype": "uint8",
    })

    with rasterio.open(output_path, "w", **profile) as dst:
        dst.write(pct_raster, 1)
        dst.write_colormap(
            1,
            {i: (int(p[0]), int(p[1]), int(p[2]), 255) for i, p in enumerate(palette)}
        )

    print(f"✔ Saved: {output_path.name}")


# -----------------------------------------------------------
# STEP 4 — APPLY TO ALL INPUT FILES
# -----------------------------------------------------------
print("\n🚀 Converting all TIFFs using SAME palette (with tolerance)...")

for tif in sorted(input_dir.glob("*.tif")):
    output_path = output_dir / f"{tif.stem}.tif"
    convert_with_global_palette(tif, output_path, PALETTE)

print("\n🎉 All files converted with FIXED palette + tolerance snapping!")
