"""
Analyzes landfalling hurricanes with at least Category 1 intensity by correlating sea surface
temperature to wind speed, and displays the relationship using ENSO phase–based coloring.

Author: Suchit Basineni
Date: 7/24/24
"""

import pandas as pd
import matplotlib.pyplot as plt

file_path = 'HurricaneData/hurricaneOne.csv'
data = pd.read_csv(file_path)

filtered_data = data[
    (data['LANDFALL'] != 0) &
    (data['SST'] >= 15) &
    (data['USA_SSHS'] >= 1.0)
]

wind_speed = pd.to_numeric(filtered_data['WMO_WIND'], errors='coerce')
sst = pd.to_numeric(filtered_data['SST'], errors='coerce')
enso = filtered_data['ENSO_Value']

colors = enso.apply(
    lambda x: 'red' if x > 0.5 else ('blue' if x < -0.5 else 'gray')
)

plt.figure(figsize=(10, 6))
plt.scatter(sst, wind_speed, c=colors, alpha=0.5, s=5)
plt.xlabel('Sea Surface Temperature (°C)', fontsize=10, labelpad=2, fontweight='bold')
plt.ylabel('Hurricane Wind Speed', fontsize=10, labelpad=7, fontweight='bold')
plt.title(
    'Sea Surface Temperature vs. Hurricane Wind Speed with ENSO Values',
    fontsize=12,
    fontweight='bold'
)
plt.grid(True)
plt.ylim(0, max(wind_speed) + 10)
plt.show()
