import matplotlib.pyplot as plt
import pandas as pd

# Define the file path
file_path = 'HurricaneData/ENSO.txt'  # Replace with the actual file path

# Read the file content
with open(file_path, 'r') as file:
    data = file.readlines()

# Remove any extra whitespace and split into lines
lines = [line.strip() for line in data if line.strip()]

# Parse the data into a dictionary
years = []
values = []
for line in lines:
    parts = line.split()
    try:
        year = parts[0]
        # Check if the line is the header, skip if it is
        if year == 'from':
            continue
        # Filter the data to only include years from 1950 to 2024
        if 1950 <= int(year) <= 2024:
            years.append(int(year))
            values.append([float(x) for x in parts[1:]])
    except ValueError:
        print("Skipped line:", line)  # Print the line that couldn't be parsed

# Create a DataFrame
df = pd.DataFrame(values, index=years)

# Transpose the DataFrame so that columns represent years and rows represent months
df_transposed = df.T
df_transposed.columns = years

# Create a new DataFrame to store the data in long format
data_long = []
for year in df_transposed.columns:
    for month in df_transposed.index:
        data_long.append([year, month + 1, df_transposed.at[month, year]])

df_long = pd.DataFrame(data_long, columns=['Year', 'Month', 'Value'])

# Plot
plt.figure(figsize=(15, 8))
for month in range(1, 13):
    subset = df_long[df_long['Month'] == month]
    colors = ['red' if val > 0 else 'blue' for val in subset['Value']]
    plt.bar(subset['Year'] + (month - 1) / 12, subset['Value'], 
            width=0.07, color=colors, align='center')

plt.xlabel('Year')
plt.ylabel('MEI.V2')
plt.title('Multivariate ENSO Index')
plt.axhline(0, color='black', linewidth=0.8)
plt.grid(True)
plt.tight_layout()
plt.show()
