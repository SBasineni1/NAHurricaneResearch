"""
Adds sea surface temperature (SST) values from a monthly mean NetCDF dataset to
North Atlantic IBTrACS hurricane records based on nearest spatial coordinates
and writes the augmented dataset to a CSV.

Author: Suchit Basineni
Date: 7/24/24
"""

import pandas as pd
import xarray as xr
import numpy as np

sst_file_path = 'HurricaneData/sst.mnmean.nc'
sst_data = xr.open_dataset(sst_file_path)
print(sst_data)

sst_data = sst_data.assign_coords(lon=(((sst_data.lon + 180) % 360) - 180))
sst_data = sst_data.sortby(sst_data.lon)
sst_data = sst_data.sortby(sst_data.lat)

ibtracs_file_path = 'HurricaneData/ibtracs.NA.list.v04r00.csv'
ibtracs_data = pd.read_csv(ibtracs_file_path, low_memory=False)

sst = sst_data['sst']

def find_nearest(array, value):
    idx = (np.abs(array - value)).argmin()
    return idx

def get_sst_value(lat, lon, time_index=0):
    lat_idx = find_nearest(sst_data['lat'].values, lat)
    lon_idx = find_nearest(sst_data['lon'].values, lon)
    return sst[time_index, lat_idx, lon_idx].values

ibtracs_data['SST'] = ibtracs_data.apply(
    lambda row: get_sst_value(row['LAT'], row['LON']),
    axis=1
)

updated_ibtracs_file_path = 'HurricaneData/HurricaneOne.csv'
ibtracs_data.to_csv(updated_ibtracs_file_path, index=False)

print(f"Updated IBTrACS CSV file saved to {updated_ibtracs_file_path}")
