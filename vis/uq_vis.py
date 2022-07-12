import pandas as pd
import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt

data = "/Users/osoro/Codebase/globalsat/results/"
results = "/Users/osoro/Codebase/globalsat/vis/"

df = pd.read_csv(data + "uq_results.csv")

# Select the required columns.
df = df[["constellation", "signal_path", "satellite_coverage_area_km", 
         "path_loss", "losses", "antenna_gain", "eirp_dB", "received_power_dB", 
         "cnr", "spectral_efficiency","agg_capacity", "capacity_per_area_mbps/sqkm"]]

# Rename columns.
df.columns = ["Constellation", "Signal path(km)","Satellite coverage area(km)", 
              "Path Loss(dB)", "Losses(dB)", "Antenna gain(dB)",
              "EIRP (dB)", "Received power(dB)", "CNR(dB)", 
              "Spectral Efficiency(bits/hertz)","Aggregate Capacity(Mbps)",
              "Capacity per area (Mbps/km^2)"]

# Plot the Heatmap. 
plt.figure(figsize=(20,15))
corr = df.corr()
matrix = np.triu(corr)
sns.set(font_scale=2)
sns.heatmap(corr,annot=True, mask=matrix, annot_kws={"size": 16}, cmap="GnBu")
plt.title("Aggregate Capacity Heatmap", fontsize = 25, fontfamily = "Helvetica")
plt.tight_layout()
plt.savefig(results + "aggregate_heatmap.jpg", dpi = 480)

# Uncertainity_plots.
x_axis = ["Constellation", "Signal path(km)", "Path Loss(dB)", 
          "Losses(dB)", "Antenna gain(dB)", "EIRP (dB)", 
          "Received power(dB)", "CNR(dB)"]

for ax in x_axis:
    plt.figure(figsize=(20,15))
    sns.set(font_scale=2)
    sns.jointplot(x = ax, y = "Aggregate Capacity(Mbps)", 
                  kind = "scatter", data = df, cmap="GnBu")
    plt.tight_layout()
    plt.savefig(results + str(ax) + ".jpg", dpi = 480)