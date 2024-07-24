import pandas as pd
import matplotlib.pyplot as plt

# Read the data into a DataFrame
file_path = 'Hurricanedata/AMO.txt'
df = pd.read_csv(file_path, delim_whitespace=True, skiprows=1, names=['Year', 'Month', 'SSTA'])

# Calculate the annual average SSTA
annual_avg_ssta = df.groupby('Year')['SSTA'].mean().reset_index()

colors = ['blue' if ssta < 0 else 'red' for ssta in annual_avg_ssta['SSTA']]

# Plot the results
plt.figure(figsize=(10, 6))
ax = plt.gca()  # Get the current axes
ax.set_facecolor('#e8e8e8')  # Set the background color of the plot area
plt.bar(annual_avg_ssta['Year'], annual_avg_ssta['SSTA'], color=colors)
plt.title('Atlantic Multidecadal Oscillation: AMO, (1854-2024)', fontsize=12, fontweight='bold')
plt.xlabel('Year',fontsize=10, labelpad=7, fontweight='bold')
plt.ylabel('Annual AMO Index',fontsize=10, labelpad=2, fontweight='bold')
plt.axhline(y=0, color='black')
plt.xlim(1854, 2024)
plt.grid(True)
plt.show()
