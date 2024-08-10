import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Define the file path
file_path = 'HurricaneData/Omon_CESM2-WACCM_ssp585_r1i1p1f1_gr_201501-210012.nc'

# Open the dataset using xarray
ds = xr.open_dataset(file_path)

# Extract the sea surface temperature (SST) data
sst = ds['tos']

# Define the Atlantic basin region (approximate lat/lon bounds)
lat_bounds = slice(0, 65)  # Latitude range from 0 to 65 degrees North
lon_bounds = slice(280, 360)  # Longitude range from 280 to 360 degrees

# Select data within the specified lat/lon bounds
atlantic_sst = sst.sel(lat=lat_bounds, lon=lon_bounds)

# Select data from 2015 to 2100
time_bounds = slice('2015-01-01', '2100-12-31')
atlantic_sst = atlantic_sst.sel(time=time_bounds)

# Compute the mean SST over the Atlantic basin
mean_atlantic_sst = atlantic_sst.mean(dim=['lat', 'lon'])

# Convert cftime objects to numpy datetime64
mean_atlantic_sst['time'] = mean_atlantic_sst.indexes['time'].to_datetimeindex()

# Create a DataFrame from the DataArray
df = mean_atlantic_sst.to_dataframe().reset_index()

# Extract year and month from the time
df['year'] = df['time'].dt.year
df['month'] = df['time'].dt.month

# Set up the plot
plt.figure(figsize=(10, 5))

# Define colors for each year using a rainbow gradient
colors = plt.cm.jet(np.linspace(0, 1, len(df['year'].unique())))

# Plot each year
for i, year in enumerate(df['year'].unique()):
    yearly_data = df[df['year'] == year]
    plt.plot(yearly_data['month'], yearly_data['tos'], color=colors[i], label=str(year))

ax = plt.gca()  # Get the current axes
ax.set_facecolor('#e8e8e8') 
plt.xlabel('Month', fontsize=10, labelpad=2, fontweight='bold')
plt.ylabel('Sea Surface Temperature (°C)', fontsize=10, labelpad=7, fontweight='bold')
plt.title('Projected North Atlantic Sea Surface Temperature (2015-2100)', fontsize=12, fontweight='bold')
plt.xticks(ticks=np.arange(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

# Set the x-axis limits to remove extra space
plt.xlim(1, 12)

# Adding a legend with a smaller number of entries to avoid clutter
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), ncol=15, loc='lower center', fontsize='small', bbox_to_anchor=(0.5, -0.325))

# Show grid
plt.grid(True)

# Display the plot
plt.show()
