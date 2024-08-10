import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
file_path = "HurricaneData/sst.mnmean.nc"  # Update with your file path
dataset = xr.open_dataset(file_path)

# Select the time range from 1950 to the latest data available in the dataset
start_time = '1950-01-01'
end_time = dataset.time.max().data
subset = dataset.sel(time=slice(start_time, end_time))

# Calculate the mean sea surface temperature for the dataset
weights = np.cos(np.deg2rad(subset.lat))
weights.name = "weights"
mean_sst = subset.sst.weighted(weights).mean(dim=['lat', 'lon'])

# Group the data by month and year
sst_by_year_month = mean_sst.groupby('time.year').apply(lambda x: x.groupby('time.month').mean(dim='time'))

# Create a new plot
plt.figure(figsize=(15, 10))

# Define months and generate colors for each year
months = np.arange(1, 13)
years = np.arange(1950, 2025)
colors = plt.cm.jet(np.linspace(0, 1, len(years)))

# Plot the data
for i, year in enumerate(years):
    plt.plot(months, sst_by_year_month.sel(year=year), color=colors[i], alpha=0.7, label=str(year))

# Set month names as x-ticks
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
plt.xticks(ticks=months, labels=month_names)

# Set x-axis limits to remove gaps
plt.xlim(1, 12)

# Set plot labels and title
plt.xlabel('Month', fontsize=10, labelpad=2, fontweight='bold')
plt.ylabel('Sea Surface Temperature (°C)', fontsize=10, labelpad=7, fontweight='bold')
plt.title('Historical North Atlantic Sea Surface Temperature (1950-2024)', fontsize=12, fontweight='bold')

# Add a legend
plt.legend(title='Year', ncol=10, bbox_to_anchor=(0.5, -0.45), loc='lower center', fontsize='small')

# Display the plot
plt.tight_layout()
plt.show()
