"""
Loads monthly mean SST data, computes an area-weighted North Atlantic mean SST from 1950 onward,
aggregates values by year and month, and plots each year’s monthly SST seasonal cycle for 1950–2024.

Author: Suchit Basineni
Date: 7/24/24
"""

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

file_path = "HurricaneData/sst.mnmean.nc"
dataset = xr.open_dataset(file_path)

start_time = '1950-01-01'
end_time = dataset.time.max().data
subset = dataset.sel(time=slice(start_time, end_time))

weights = np.cos(np.deg2rad(subset.lat))
weights.name = "weights"
mean_sst = subset.sst.weighted(weights).mean(dim=['lat', 'lon'])

sst_by_year_month = mean_sst.groupby('time.year').apply(
    lambda x: x.groupby('time.month').mean(dim='time')
)

plt.figure(figsize=(15, 10))

months = np.arange(1, 13)
years = np.arange(1950, 2025)
colors = plt.cm.jet(np.linspace(0, 1, len(years)))

for i, year in enumerate(years):
    plt.plot(
        months,
        sst_by_year_month.sel(year=year),
        color=colors[i],
        alpha=0.7,
        label=str(year)
    )

month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
plt.xticks(ticks=months, labels=month_names)
plt.xlim(1, 12)

plt.xlabel('Month', fontsize=10, labelpad=2, fontweight='bold')
plt.ylabel('Sea Surface Temperature (°C)', fontsize=10, labelpad=7, fontweight='bold')
plt.title('Historical North Atlantic Sea Surface Temperature (1950-2024)', fontsize=12, fontweight='bold')

plt.legend(title='Year', ncol=10, bbox_to_anchor=(0.5, -0.45), loc='lower center', fontsize='small')

plt.tight_layout()
plt.show()
