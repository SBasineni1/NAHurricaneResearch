import pandas as pd

# Load dataset from CSV file
df = pd.read_csv('HurricaneData/ibtracs.NA.list.v04r00.csv')

# Convert the 'SEASON' column to numeric, forcing errors to NaN
df['SEASON'] = pd.to_numeric(df['SEASON'], errors='coerce')

# Remove rows with NaN values in the 'SEASON' column (if any)
df = df.dropna(subset=['SEASON'])

# Convert the 'SEASON' column to integer
df['SEASON'] = df['SEASON'].astype(int)

# Remove rows where the SEASON is not between 1950 and 2024
df_filtered = df[(df['SEASON'] >= 1950) & (df['SEASON'] <= 2024)]

# Save the filtered dataset to a new CSV file
df_filtered.to_csv('HurricaneData/ibtracs.NA.list.v04r00.csv', index=False)

print("Filtered dataset has been saved to 'filtered_dataset.csv'")
