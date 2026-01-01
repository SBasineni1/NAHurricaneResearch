"""
Loads CESM2-WACCM SSP5-8.5 sea surface temperature projections, computes the monthly mean SST
over the North Atlantic basin (0–65°N, 280–360°E) for 2015–2100, and plots each year’s seasonal
cycle.

Author: Suchit Basineni
Date: 7/24/24
"""

import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

file_path = 'HurricaneData/Omon_CESM2-WACCM_ssp585_r1i1p1f1_gr_201501-210012.nc'
ds = xr.open_dataset(file_path)

sst = ds['tos']

lat_bounds = slice(0, 65)
lon_bounds = slice(280, 360)

atlantic_sst = sst.sel(lat=lat_bounds, lon=lon_bounds)

time_bounds = slice('2015-01-01', '2100-12-31')
atlantic_sst = atlantic_sst.sel(time=time_bounds)

mean_atlantic_sst = atlantic_sst.mean(dim=['lat', 'lon'])
mean_atlantic_sst['time'] = mean_atlantic_sst.indexes['time'].to_datetimeindex()

df = mean_atlantic_sst.to_dataframe().reset_index()
df['year'] = df['time'].dt.year
df['month'] = df['time'].dt.month

plt.figure(figsize=(10, 5))

colors = plt.cm.jet(np.linspace(0, 1, len(df['year'].unique())))

for i, year in enumerate(df['year'].unique()):
    yearly_data = df[df['year'] == year]
    plt.plot(yearly_data['month'], yearly_data['tos'], color=colors[i], label=str(year))

ax = plt.gca()
ax.set_facecolor('#e8e8e8')
plt.xlabel('Month', fontsize=10, labelpad=2, fontweight='bold')
plt.ylabel('Sea Surface Temperature (°C)', fontsize=10, labelpad=7, fontweight='bold')
plt.title('Projected North Atlantic Sea Surface Temperature (2015-2100)', fontsize=12, fontweight='bold')
plt.xticks(
    ticks=np.arange(1, 13),
    labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
)
plt.xlim(1, 12)

handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(
    by_label.values(),
    by_label.keys(),
    ncol=15,
    loc='lower center',
    fontsize='small',
    bbox_to_anchor=(0.5, -0.325)
)

plt.grid(True)
plt.show()
