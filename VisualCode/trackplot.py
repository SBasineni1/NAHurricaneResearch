"""
Loads North Atlantic hurricane track data, filters records to 1950–2023 La Niña conditions, builds 3-hr storm track segments
and intensity-colored points, and plots the resulting tracks on a basemap with a category legend.

Author: Suchit Basineni
Date: 7/24/24
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import contextily as ctx
from matplotlib.lines import Line2D

file_path = 'HurricaneData/HurricaneTracks.csv'
data = pd.read_csv(file_path, low_memory=False)

data['ISO_TIME'] = pd.to_datetime(data['ISO_TIME'], errors='coerce')

data_filtered = data[data['ISO_TIME'].dt.year.between(1950, 2023)]
data_filtered = data_filtered[data_filtered['ENSO_Value'] <= -0.5]

data_filtered['LAT'] = pd.to_numeric(data_filtered['LAT'], errors='coerce')
data_filtered['LON'] = pd.to_numeric(data_filtered['LON'], errors='coerce')

data_filtered = data_filtered.dropna(subset=['LAT', 'LON'])

data_filtered = data_filtered[
    (data_filtered['LAT'] >= -90) & (data_filtered['LAT'] <= 90) &
    (data_filtered['LON'] >= -180) & (data_filtered['LON'] <= 180)
]

print(f"Total entries in the dataset: {len(data)}")
print(f"Entries for the years 2010-2019 in October: {len(data_filtered)}")

gdf_points = gpd.GeoDataFrame(
    data_filtered,
    geometry=gpd.points_from_xy(data_filtered['LON'], data_filtered['LAT']),
    crs="EPSG:4326"
)

strength_colors = {
    -1: 'blue',
    0: 'green',
    1: 'yellow',
    2: 'orange',
    3: 'red',
    4: 'magenta',
    5: '#A020F0',
}

gdf_points['color'] = gdf_points['USA_SSHS'].map(strength_colors).fillna('grey')

lines = []
for name, group in data_filtered.groupby('SID'):
    group = group.sort_values('ISO_TIME')
    coords = []
    for i in range(len(group) - 1):
        if (group['ISO_TIME'].iloc[i + 1] - group['ISO_TIME'].iloc[i]).total_seconds() <= 6 * 3600:
            coords.append((group['LON'].iloc[i], group['LAT'].iloc[i]))
        else:
            if len(coords) > 1:
                line = LineString(coords)
                lines.append({'geometry': line, 'color': 'black'})
            coords = [(group['LON'].iloc[i + 1], group['LAT'].iloc[i + 1])]
    if len(coords) > 1:
        line = LineString(coords)
        lines.append({'geometry': line, 'color': 'black'})

gdf_lines = gpd.GeoDataFrame(lines, crs="EPSG:4326")

if gdf_points.empty:
    print("No data available for plotting.")
else:
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))

    gdf_lines.plot(ax=ax, color='black', alpha=0.35, zorder=1)
    gdf_points.plot(ax=ax, color=gdf_points['color'], markersize=5, zorder=2)

    ctx.add_basemap(ax, crs=gdf_points.crs.to_string(), source=ctx.providers.Esri.WorldImagery)

    ax.set_xlim([-100, -50])
    ax.set_ylim([10, 50])

    plt.title('1950-2019 La Niña North Atlantic Hurricanes', fontsize=12, fontweight='bold')
    plt.xlabel('Longitude', fontsize=10, labelpad=7, fontweight='bold')
    plt.ylabel('Latitude', fontsize=10, labelpad=2, fontweight='bold')

    legend_elements = [
        Line2D([0], [0], marker='o', color='black', label='Category 1', markersize=10, markerfacecolor='yellow'),
        Line2D([0], [0], marker='o', color='black', label='Category 2', markersize=10, markerfacecolor='orange'),
        Line2D([0], [0], marker='o', color='black', label='Category 3', markersize=10, markerfacecolor='red'),
        Line2D([0], [0], marker='o', color='black', label='Category 4', markersize=10, markerfacecolor='magenta'),
        Line2D([0], [0], marker='o', color='black', label='Category 5', markersize=10, markerfacecolor='#A020F0')
    ]
    ax.legend(handles=legend_elements, loc='lower right')

    plt.savefig('hurricane_2010_2019_october_atlantic.png')
    plt.show()
