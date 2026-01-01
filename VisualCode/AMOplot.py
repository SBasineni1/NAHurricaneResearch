"""
Loads monthly AMO index values, computes annual mean sea surface temperature anomaly (SSTA),
and generates a bar chart of the annual AMO index for 1854–2024.

Author: Suchit Basineni
Date: 7/24/24
"""

import pandas as pd
import matplotlib.pyplot as plt

file_path = 'Hurricanedata/AMO.txt'
df = pd.read_csv(file_path, delim_whitespace=True, skiprows=1, names=['Year', 'Month', 'SSTA'])

annual_avg_ssta = df.groupby('Year')['SSTA'].mean().reset_index()
colors = ['blue' if ssta < 0 else 'red' for ssta in annual_avg_ssta['SSTA']]

plt.figure(figsize=(10, 6))
ax = plt.gca()
ax.set_facecolor('#e8e8e8')
plt.bar(annual_avg_ssta['Year'], annual_avg_ssta['SSTA'], color=colors)
plt.title('Atlantic Multidecadal Oscillation: AMO, (1854-2024)', fontsize=12, fontweight='bold')
plt.xlabel('Year', fontsize=10, labelpad=7, fontweight='bold')
plt.ylabel('Annual AMO Index', fontsize=10, labelpad=2, fontweight='bold')
plt.axhline(y=0, color='black')
plt.xlim(1854, 2024)
plt.grid(True)
plt.show()
