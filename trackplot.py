import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString

# Load the CSV file
file_path = 'HurricaneData/ibtracs.NA.list.v04r00.csv'
data = pd.read_csv(file_path, low_memory=False)

# Ensure 'ISO_TIME' is in datetime format
data['ISO_TIME'] = pd.to_datetime(data['ISO_TIME'], errors='coerce')

# Filter data for the year 2022
data_2022 = data[data['ISO_TIME'].dt.year == 2023]

# Filter data for the Atlantic Ocean and specific hurricane 'OPHELIA'
data_atlantic_2022 = data_2022[data_2022['NAME'] == 'OPHELIA']

# Convert latitude and longitude to numeric, coercing errors
data_atlantic_2022['LAT'] = pd.to_numeric(data_atlantic_2022['LAT'], errors='coerce')
data_atlantic_2022['LON'] = pd.to_numeric(data_atlantic_2022['LON'], errors='coerce')

# Drop rows with invalid coordinates
data_atlantic_2022 = data_atlantic_2022.dropna(subset=['LAT', 'LON'])

# Ensure valid latitude and longitude ranges
data_atlantic_2022 = data_atlantic_2022[
    (data_atlantic_2022['LAT'] >= -90) & (data_atlantic_2022['LAT'] <= 90) &
    (data_atlantic_2022['LON'] >= -180) & (data_atlantic_2022['LON'] <= 180)
]

# Debugging output
print(f"Total entries in the dataset: {len(data)}")
print(f"Entries for the year 2022: {len(data_2022)}")
print(f"Entries for the Atlantic basin in 2022: {len(data_atlantic_2022)}")

# Create a GeoDataFrame for points
gdf_points = gpd.GeoDataFrame(data_2022, 
                              geometry=gpd.points_from_xy(data_2022['LON'], data_2022['LAT']),
                              crs="EPSG:4326")


# Create a GeoDataFrame for lines
lines = []
for name, group in data_2022.groupby('NAME'):
    group = group.sort_values('ISO_TIME')
    if len(group) > 1:
        line = LineString(zip(group['LON'], group['LAT']))
        lines.append({'geometry': line, 'color': 'black'})  # Black color for lines

gdf_lines = gpd.GeoDataFrame(lines, crs="EPSG:4326")

# Define colors based on hurricane strength
strength_colors = {
    -1: 'blue',   # Tropical Depression
    0: 'green',
    1: 'yellow',  # Category 1
    2: 'orange',  # Category 2
    3: 'red',     # Category 3
    4: 'magenta', # Category 4
    5: '#A020F0', # Category 5
}

# Map colors to the data based on the 'USA_SSHS' column
gdf_points['color'] = gdf_points['USA_SSHS'].map(strength_colors).fillna('grey')  # 'grey' for undefined/unknown categories

# Check if gdf_points is empty
if gdf_points.empty:
    print("No data available for plotting.")
else:
    # Read Natural Earth data
    read_data = 'HurricaneData/e_110m_admin_0_countries.zip'
    world = gpd.read_file(read_data)

    # Plotting
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    world.boundary.plot(ax=ax)
    
    # Plot lines using matplotlib directly
    for line in gdf_lines['geometry']:
        ax.plot(*line.xy, color='black', alpha=0.2)

    # Plot points
    gdf_points.plot(ax=ax, color=gdf_points['color'], markersize=5)

    ax.set_xlim([-100, 0])
    ax.set_ylim([5, 50])

    plt.title('2023 Atlantic Ocean Hurricanes')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    # Save the plot to a file
    plt.savefig('hurricane_ophelia_2022_atlantic.png')

    # Show the plot
    plt.show()
