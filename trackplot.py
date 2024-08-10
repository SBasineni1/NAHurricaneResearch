import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import contextily as ctx
from matplotlib.lines import Line2D

# Load the CSV file
file_path = 'HurricaneData/HurricaneTracks.csv'
data = pd.read_csv(file_path, low_memory=False)

# Ensure 'ISO_TIME' is in datetime format
data['ISO_TIME'] = pd.to_datetime(data['ISO_TIME'], errors='coerce')

# Filter data for the years 1950-1960
data_filtered = data[data['ISO_TIME'].dt.year.between(2020, 2023)]

# Convert latitude and longitude to numeric, coercing errors
data_filtered['LAT'] = pd.to_numeric(data_filtered['LAT'], errors='coerce')
data_filtered['LON'] = pd.to_numeric(data_filtered['LON'], errors='coerce')

# Drop rows with invalid coordinates
data_filtered = data_filtered.dropna(subset=['LAT', 'LON'])

# Ensure valid latitude and longitude ranges
data_filtered = data_filtered[
    (data_filtered['LAT'] >= -90) & (data_filtered['LAT'] <= 90) &
    (data_filtered['LON'] >= -180) & (data_filtered['LON'] <= 180)
]

# Debugging output
print(f"Total entries in the dataset: {len(data)}")
print(f"Entries for the years 1950-1960: {len(data_filtered)}")

# Create a GeoDataFrame for points
gdf_points = gpd.GeoDataFrame(data_filtered, 
                              geometry=gpd.points_from_xy(data_filtered['LON'], data_filtered['LAT']),
                              crs="EPSG:4326")

# Define colors based on hurricane strength
strength_colors = {
    -1: 'blue',   # Tropical Depression
    0: 'green',   # Tropical Storm
    1: 'yellow',  # Category 1
    2: 'orange',  # Category 2
    3: 'red',     # Category 3
    4: 'magenta', # Category 4
    5: '#A020F0', # Category 5
}

# Map colors to the data based on the 'USA_SSHS' column
gdf_points['color'] = gdf_points['USA_SSHS'].map(strength_colors).fillna('grey')  # 'grey' for undefined/unknown categories

# Create a GeoDataFrame for lines
lines = []
for name, group in data_filtered.groupby('SID'):
    group = group.sort_values('ISO_TIME')
    coords = []
    for i in range(len(group) - 1):
        if (group['ISO_TIME'].iloc[i+1] - group['ISO_TIME'].iloc[i]).total_seconds() <= 6 * 3600:
            coords.append((group['LON'].iloc[i], group['LAT'].iloc[i]))
        else:
            if len(coords) > 1:
                line = LineString(coords)
                lines.append({'geometry': line, 'color': 'black'})  # Black color for lines
            coords = [(group['LON'].iloc[i+1], group['LAT'].iloc[i+1])]
    if len(coords) > 1:
        line = LineString(coords)
        lines.append({'geometry': line, 'color': 'black'})

gdf_lines = gpd.GeoDataFrame(lines, crs="EPSG:4326")

# Check if gdf_points is empty
if gdf_points.empty:
    print("No data available for plotting.")
else:
# Plotting
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))

    # Plot lines with lower opacity
    gdf_lines.plot(ax=ax, color='black', alpha=0.35, zorder=1)  # Set zorder for lines

    # Plot points over lines with higher zorder
    gdf_points.plot(ax=ax, color=gdf_points['color'], markersize=5, zorder=2)  # Higher zorder for points

    # Add basemap with contextily
    ctx.add_basemap(ax, crs=gdf_points.crs.to_string(), source=ctx.providers.Esri.WorldImagery)

    ax.set_xlim([-100, -50])
    ax.set_ylim([10, 50])

    plt.title('2020-2023 North Atlantic Tropical Cyclones', fontsize=12, fontweight='bold')
    plt.xlabel('Longitude', fontsize=10, labelpad=7, fontweight='bold')
    plt.ylabel('Latitude', fontsize=10, labelpad=2, fontweight='bold')

    # Create custom legend
    legend_elements = [
        Line2D([0], [0], marker='o', color='black', label='Category 1', markersize=10, markerfacecolor='yellow'),
        Line2D([0], [0], marker='o', color='black', label='Category 2', markersize=10, markerfacecolor='orange'),
        Line2D([0], [0], marker='o', color='black', label='Category 3', markersize=10, markerfacecolor='red'),
        Line2D([0], [0], marker='o', color='black', label='Category 4', markersize=10, markerfacecolor='magenta'),
        Line2D([0], [0], marker='o', color='black', label='Category 5', markersize=10, markerfacecolor='#A020F0')
    ]
    ax.legend(handles=legend_elements, loc='lower right')

    # Save the plot to a file
    plt.savefig('hurricane_1950_1960_atlantic.png')

    # Show the plot
    plt.show()
