"""
Parses extended ENSO/ONI monthly anomaly data from a text file, counts the number of months in
La Nina / Neutral / El Nino conditions using fixed thresholds, and plots monthly anomalies by year.

Author: Suchit Basineni
Date: 7/24/24
"""

import matplotlib.pyplot as plt
import pandas as pd

file_path = 'HurricaneData/ENSO_extended.txt'

with open(file_path, 'r') as file:
    data = file.readlines()

lines = [line.strip() for line in data if line.strip()]

years = []
values = []
for line in lines:
    parts = line.split()
    try:
        year = parts[0]
        if year == 'from':
            continue
        if 1900 <= int(year) <= 2024:
            years.append(int(year))
            values.append([float(x) for x in parts[1:]])
    except ValueError:
        print("Skipped line:", line)

df = pd.DataFrame(values, index=years)

df_transposed = df.T
df_transposed.columns = years

data_long = []
for year in df_transposed.columns:
    for month in df_transposed.index:
        data_long.append([year, month + 1, df_transposed.at[month, year]])

df_long = pd.DataFrame(data_long, columns=['Year', 'Month', 'Value'])

la_nina_threshold = -0.5
el_nino_threshold = 0.5

la_nina_months = 0
neutral_months = 0
el_nino_months = 0

for value in df_long['Value']:
    if value < la_nina_threshold:
        la_nina_months += 1
    elif value > el_nino_threshold:
        el_nino_months += 1
    else:
        neutral_months += 1

print(f"Total months of La Niña conditions (Value < {la_nina_threshold}): {la_nina_months}")
print(f"Total months of ENSO Neutral conditions ({la_nina_threshold} <= Value <= {el_nino_threshold}): {neutral_months}")
print(f"Total months of El Niño conditions (Value > {el_nino_threshold}): {el_nino_months}")

plt.figure(figsize=(15, 8))
for month in range(1, 13):
    subset = df_long[df_long['Month'] == month]
    colors = ['red' if val > 0 else 'blue' for val in subset['Value']]
    plt.bar(
        subset['Year'] + (month - 1) / 12,
        subset['Value'],
        width=0.07,
        color=colors,
        align='center'
    )

plt.xlim([min(years), max(years)])

plt.xlabel('Year', fontsize=10, labelpad=2, fontweight='bold')
plt.ylabel('Anomaly', fontsize=10, labelpad=7, fontweight='bold')
plt.title('Oceanic Niño Index (ONI)', fontsize=12, fontweight='bold')
plt.axhline(0, color='black', linewidth=0.8)
plt.grid(True)
plt.tight_layout()
plt.show()
