import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
dataset_path = "HurricaneData/sst.mon.mean.nc"  # Replace with the actual path to your dataset
ds = xr.open_dataset(dataset_path, decode_times=False)

# Select the region from 0°N to 65°N and 280°E to 360°E
sst = ds['sst'].sel(lat=slice(0, 65), lon=slice(280, 360))

# Compute the mean SST over the selected latitude and longitude range
sst_mean = sst.mean(dim=['lat', 'lon'])

# Dataset starts from September 1981 and ends in July 2024
start_year, start_month = 1981, 9
end_year, end_month = 2024, 7

# Calculate the expected number of months
expected_months = (end_year - start_year) * 12 + (end_month - start_month + 1)

# Actual number of months in the dataset
actual_months = len(sst_mean)

# Initialize a full SST array with NaNs
sst_full = np.full(expected_months, np.nan)

# Create an array representing the actual time series, starting at index 8 (corresponding to Sep 1981)
time_series_actual = np.arange(8, 8 + actual_months)

# Trim time_series_actual to stay within bounds of sst_full
if time_series_actual[-1] >= len(sst_full):
    time_series_actual = time_series_actual[:len(sst_full)]

# Trim sst_values accordingly
sst_values = sst_mean.values[:len(time_series_actual)]

# Print the first few values of the mean SST over time
print(ds)


# Place the actual SST data into the full array
sst_full[time_series_actual] = sst_values

# Interpolate missing data
sst_full = np.interp(np.arange(len(sst_full)), time_series_actual, sst_full[time_series_actual])

# Reshape the SST data so that each row corresponds to one year and each column to one month
sst_reshaped = sst_full.reshape((-1, 12))

# Plotting
fig, ax = plt.subplots(figsize=(14, 8))

# Get the colormap and set the number of discrete colors
cmap = plt.colormaps.get_cmap('rainbow')
colors = cmap(np.linspace(0, 1, sst_reshaped.shape[0]))

# Plot each year's data with corresponding color
for i in range(sst_reshaped.shape[0]):
    ax.plot(np.arange(1, 13), sst_reshaped[i, :], label=f"{1981 + i}", color=colors[i])

# Add labels and title
ax.set_facecolor('#e8e8e8')
ax.set_xlabel("Month", fontsize=10, labelpad=2, fontweight='bold')
ax.set_ylabel("Sea Surface Temperature (°C)", fontsize=10, labelpad=7, fontweight='bold')
ax.set_title("Monthly Sea Surface Temperature, North Atlantic Basin (0°N-65°N, 0°W-80°W)", fontsize=12, fontweight='bold')
ax.legend(title="Year", bbox_to_anchor=(0.5, -0.25), loc='lower center', fontsize='small', ncol=15)
ax.grid(True)

# Set x-axis limits to remove empty space
ax.set_xlim(1, 12)

# Set month names as x-axis labels
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
ax.set_xticks(np.arange(1, 13))
ax.set_xticklabels(month_names)

# Adjust layout to remove white spaces
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.1)
plt.tight_layout()

# Display the plot
plt.show()
