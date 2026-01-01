import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
df = pd.read_csv("Hydrological_Analysis_UTM_Fixed.csv")

# Remove missing values if present
df = df.dropna(subset=["Season", "Rain_0_5km", "River_Width_m"])

# --------------------------------------------------
# UNIQUE SEASONS
# --------------------------------------------------
seasons = df["Season"].unique()

# --------------------------------------------------
# PLOT SEASON-WISE SCATTER + BEST FIT LINE + YEAR LABELS
# --------------------------------------------------
for season in seasons:
    sub = df[df["Season"] == season]

    X = sub["Rain_0_5km"].values
    Y = sub["River_Width_m"].values
    years = sub["Year"].values    # <-- year column

    # Fit line: y = m*x + c
    m, c = np.polyfit(X, Y, 1)
    line = m * X + c

    plt.figure(figsize=(8, 6))
    plt.scatter(X, Y, label="River Width", alpha=0.7)

    # ---- Add Year Labels for each point ----
    for xi, yi, yr in zip(X, Y, years):
        plt.text(xi, yi, str(yr), fontsize=9, ha='left', va='bottom')

    # ---- Best-fit line ----
    plt.plot(X, line, label=f"Best Fit Line (Slope={m:.4f})")

    plt.title(f"Season-wise Scatter Plot: Rainfall vs River Width ({season})")
    plt.xlabel("Rainfall (mm)")
    plt.ylabel("River Width (m)")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.savefig(f"Rainfall_vs_RiverWidth_{season}.png", dpi=300)
    plt.show()
