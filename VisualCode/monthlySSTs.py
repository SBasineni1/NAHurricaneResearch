"""
Loads monthly SST data from a NetCDF file, computes the North Atlantic basin mean SST (0–65°N, 280–360°E),
fills the 1981-09 to 2024-07 monthly time series via interpolation where needed, reshapes to year-by-month,
and plots each year’s seasonal SST cycle.

Author: Suchit Basineni
Date: 7/24/24
"""

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

dataset_path = "HurricaneData/sst.mon.mean.nc"
ds = xr.open_dataset(dataset_path, decode_times=False)

sst = ds['sst'].sel(lat=slice(0, 65), lon=slice(280, 360))
sst_mean = sst.mean(dim=['lat', 'lon'])

start_year, start_month = 1981, 9
end_year, end_month = 2024, 7

expected_months = (end_year - start_year) * 12 + (end_month - start_month + 1)
actual_months = len(sst_mean)

sst_full = np.full(expected_months, np.nan)

time_series_actual = np.arange(8, 8 + actual_months)

if time_series_actual[-1] >= len(sst_full):
    time_series_actual = time_series_actual[:len(sst_full)]

sst_values = sst_mean.values[:len(time_series_actual)]

print(ds)

sst_full[time_series_actual] = sst_values

sst_full = np.interp(np.arange(len(sst_full)), time_series_actual, sst_full[time_series_actual])

sst_reshaped = sst_full.reshape((-1, 12))

fig, ax = plt.subplots(figsize=(14, 8))

cmap = plt.colormaps.get_cmap('rainbow')
colors = cmap(np.linspace(0, 1, sst_reshaped.shape[0]))

for i in range(sst_reshaped.shape[0]):
    ax.plot(np.arange(1, 13), sst_reshaped[i, :], label=f"{1981 + i}", color=colors[i])

ax.set_facecolor('#e8e8e8')
ax.set_xlabel("Month", fontsize=10, labelpad=2, fontweight='bold')
ax.set_ylabel("Sea Surface Temperature (°C)", fontsize=10, labelpad=7, fontweight='bold')
ax.set_title(
    "Monthly Sea Surface Temperature, North Atlantic Basin (0°N-65°N, 0°W-80°W)",
    fontsize=12,
    fontweight='bold'
)
ax.legend(title="Year", bbox_to_anchor=(0.5, -0.25), loc='lower center', fontsize='small', ncol=15)
ax.grid(True)

ax.set_xlim(1, 12)

month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
ax.set_xticks(np.arange(1, 13))
ax.set_xticklabels(month_names)

plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.1)
plt.tight_layout()
plt.show()
