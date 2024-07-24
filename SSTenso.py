import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'HurricaneData/hurricaneOne.csv'
data = pd.read_csv(file_path)

# Extract relevant columns
wind_speed = data['WMO_WIND']
sst = data['SST']
enso = data['ENSO_Value']

# Define colors based on ENSO values
colors = enso.apply(lambda x: 'red' if x > 0.5 else ('blue' if x < -0.5 else 'gray'))

# Create the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(sst, wind_speed, c=colors, alpha=0.5)
plt.xlabel('Sea Surface Temperature (SST)')
plt.ylabel('Hurricane Wind Speed (WMO_WIND)')
plt.title('Sea Surface Temperature vs. Hurricane Wind Speed with ENSO Values')
plt.grid(True)

# Show the plot
plt.show()
