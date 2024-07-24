import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the data from the CSV file
df = pd.read_csv('HurricaneData\hurricaneOne.csv')

# Function to determine color based on ENSO value
def get_color(enso_value):
    if enso_value >= 3:
        return 'red'
    elif enso_value <= -2:
        return 'blue'
    elif -0.5 <= enso_value <= 0.5:
        return 'lightgray'
    else:
        norm_value = (enso_value + 2) / 5  
        return plt.cm.coolwarm(norm_value)

colors = df['ENSO_Value_x'].apply(get_color)

hurricane_categories = {
    '1': (64, 82),
    '2': (83, 95),
    '3': (96, 112),
    '4': (113, 136),
    '5': (137, 200)  # 200 is an arbitrary upper bound
}

category_names = list(hurricane_categories.keys())
category_ticks = [np.min(bounds) for bounds in hurricane_categories.values()]

fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.scatter(df['ENSO_Value_x'], df['USA_WIND'], c=colors)
ax1.set_title('ENSO Value vs Hurricane Max Speed')
ax1.set_xlabel('ENSO Value')
ax1.set_ylabel('MAX Wind Speed (kts)')
ax1.grid(True)

ax1.set_xticks(ticks=[i * 0.5 for i in range(-4, 5)])  # Adjust the range as needed

ax2 = ax1.twinx()
ax2.set_ylabel('Hurricane Category Strength ')

ax2.set_yticks(category_ticks)
ax2.set_yticklabels(category_names)

# Optional: synchronize the y-axis range
ax2.set_ylim(ax1.get_ylim())

plt.show()
