"""
Loads hurricane-level data, visualizes the relationship between ENSO values and maximum hurricane wind speed,
adds category on the x-axis, and displays storm counts across ENSO phase thresholds.

Author: Suchit Basineni
Date: 7/24/24
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('HurricaneData/hurricaneOne.csv')

def get_color(enso_value):
    if enso_value >= 3:
        return '#FF0000'
    elif enso_value <= -2:
        return '#0000FF'
    else:
        norm_value = (enso_value + 2) / 4
        return plt.cm.coolwarm(norm_value)

colors = df['ENSO_Value_x'].apply(get_color)

hurricane_categories = {
    '1': (64, 82),
    '2': (83, 95),
    '3': (96, 112),
    '4': (113, 136),
    '5': (137, 200)
}

category_names = list(hurricane_categories.keys())
category_ticks = [np.min(bounds) for bounds in hurricane_categories.values()]

fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.scatter(df['ENSO_Value_x'], df['USA_WIND'], c=colors, s=50, alpha=1)

ax1.set_title('ENSO Value vs Hurricane Max Speed', fontsize=12, fontweight='bold')
ax1.set_xlabel('ENSO Value', fontsize=10, labelpad=2, fontweight='bold')
ax1.set_ylabel('MAX Wind Speed (kts)', fontsize=10, labelpad=7, fontweight='bold')

ax1.grid(False)
ax1.set_xticks(ticks=[i * 0.5 for i in range(-5, 6)])

ax2 = ax1.twinx()
ax2.set_ylabel('Hurricane Category Strength ', fontsize=10, labelpad=7, fontweight='bold')

plt.axhline(y=64, color='orange', alpha=0.25)
plt.axhline(y=83, color='orange', alpha=0.25)
plt.axhline(y=96, color='orange', alpha=0.25)
plt.axhline(y=113, color='orange', alpha=0.25)
plt.axhline(y=137, color='orange', alpha=0.25)

ax2.set_yticks(category_ticks)
ax2.set_yticklabels(category_names)

ax2.set_ylim(ax1.get_ylim())

count_negative = len(df[df['ENSO_Value_x'] <= -0.5])
count_neutral = len(df[(df['ENSO_Value_x'] > -0.5) & (df['ENSO_Value_x'] < 0.5)])
count_positive = len(df[df['ENSO_Value_x'] >= 0.5])

print(f"Number of hurricanes with ENSO value <= -0.5: {count_negative}")
print(f"Number of hurricanes with -0.5 < ENSO value < 0.5: {count_neutral}")
print(f"Number of hurricanes with ENSO value >= 0.5: {count_positive}")

plt.show()
