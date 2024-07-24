import pandas as pd
import xarray as xr
import numpy as np

# Load the SST NetCDF file
sst_file_path = 'HurricaneData/sst.mnmean.nc'
sst_data = xr.open_dataset(sst_file_path)

# Clean up the lat/lon coordinates
# Convert 0 to 360 longitude to -180 to 180
sst_data = sst_data.assign_coords(lon=(((sst_data.lon + 180) % 360) - 180))

# Sort lat and lon coordinates in increasing order
sst_data = sst_data.sortby(sst_data.lon)
sst_data = sst_data.sortby(sst_data.lat)


# Load the IBTrACS CSV file with specified data types
ibtracs_file_path = 'HurricaneData/ibtracs.NA.list.v04r00.csv'
ibtracs_data = pd.read_csv(ibtracs_file_path, low_memory=False)

# Extract relevant SST data (assuming monthly mean SST)
sst = sst_data['sst']

# Function to find the nearest value in an array
def find_nearest(array, value):
    idx = (np.abs(array - value)).argmin()
    return idx

# Function to get SST value for a specific latitude and longitude
def get_sst_value(lat, lon, time_index=0):
    lat_idx = find_nearest(sst_data['lat'].values, lat)
    lon_idx = find_nearest(sst_data['lon'].values, lon)
    return sst[time_index, lat_idx, lon_idx].values

# Add a new column for SST values
ibtracs_data['SST'] = ibtracs_data.apply(lambda row: get_sst_value(row['LAT'], row['LON']), axis=1)

# Save the updated IBTrACS CSV file
updated_ibtracs_file_path = 'HurricaneData/HurricaneOne.csv'
ibtracs_data.to_csv(updated_ibtracs_file_path, index=False)

print(f"Updated IBTrACS CSV file saved to {updated_ibtracs_file_path}")
