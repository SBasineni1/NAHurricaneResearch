import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'HurricaneData/hurricaneOne.csv'
data = pd.read_csv(file_path)

# Filter the data where Landfall is not equal to 0 and SST is greater than or equal to 26
filtered_data = data[(data['LANDFALL'] != 0) & (data['SST'] >= 15) & (data['USA_SSHS'] >= 1.0)]

# Extract relevant columns from the filtered data
wind_speed = pd.to_numeric(filtered_data['WMO_WIND'], errors='coerce')  # Ensure numeric values
sst = pd.to_numeric(filtered_data['SST'], errors='coerce')
enso = filtered_data['ENSO_Value']

# Define colors based on ENSO values
colors = enso.apply(lambda x: 'red' if x > 0.5 else ('blue' if x < -0.5 else 'gray'))

# Create the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(sst, wind_speed, c=colors, alpha=0.5, s=5)
plt.xlabel('Sea Surface Temperature (SST)')
plt.ylabel('Hurricane Wind Speed')
plt.title('Sea Surface Temperature vs. Hurricane Wind Speed with ENSO Values')
plt.grid(True)
plt.ylim(0, max(wind_speed) + 10)  # Ensure y-axis starts at 0 and has some space above max value

# Show the plot
plt.show()
