import pandas as pd

# ---------------------------------------------------------
# LOAD YOUR CSV FILES
# ---------------------------------------------------------
# File 1: Contains Year, Season, Rainfall_mm (or Rain_0_5km), River_Width
df_rw = pd.read_csv("Hydrological_Analysis_Clipped_Safe.csv")

# File 2: Contains Year, Season, Rainfall_mm, ReservoirArea_km2
df_res = pd.read_csv("Reservoir_vs_Rainfall.csv")

# ---------------------------------------------------------
# CLEAN COLUMN NAMES (OPTIONAL)
# ---------------------------------------------------------
df_rw.columns = df_rw.columns.str.strip()
df_res.columns = df_res.columns.str.strip()

# If your rainfall column is named differently, adjust here:
rain_col_rw = "Rainfall_mm" if "Rainfall_mm" in df_rw.columns else "Rainfall"
rain_col_res = "Rainfall_mm" if "Rainfall_mm" in df_res.columns else "Rainfall"

# ---------------------------------------------------------
# COMPUTE CORRELATIONS FOR EACH SEASON
# ---------------------------------------------------------
seasons = df_rw["Season"].unique()

results = []

for season in seasons:
    # --- Filter season-wise ---
    sub_rw = df_rw[df_rw["Season"] == season]
    sub_res = df_res[df_res["Season"] == season]
    
    # --- Compute Pearson correlations ---
    corr_rw = sub_rw[rain_col_rw].corr(sub_rw["River_Width"])
    corr_res = sub_res[rain_col_res].corr(sub_res["ReservoirArea_km2"])
    
    results.append({
        "Season": season,
        "Corr_Rain_vs_RiverWidth": corr_rw,
        "Corr_Rain_vs_ReservoirArea": corr_res
    })

# ---------------------------------------------------------
# OUTPUT RESULTS AS DATAFRAME
# ---------------------------------------------------------
df_corr = pd.DataFrame(results)
print("\n=== Season-wise Pearson Correlations ===\n")
print(df_corr.to_string(index=False))

# Optionally save output
df_corr.to_csv("seasonal_correlations.csv", index=False)
