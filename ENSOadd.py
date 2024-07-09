import pandas as pd

# Path to your CSV file
file_path = 'HurricaneData/ibtracs.NA.list.v04r00.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# Display the columns to verify the column names
print("Columns in DataFrame:", df.columns)

# Ensure 'ISO_TIME' column is present
if 'ISO_TIME' not in df.columns:
    raise KeyError("Column 'ISO_TIME' not found in the DataFrame")

# Convert 'ISO_TIME' to datetime
df['ISO_TIME'] = pd.to_datetime(df['ISO_TIME'])

# Extract year and month from 'ISO_TIME' column
df['Year'] = df['ISO_TIME'].dt.year
df['Month'] = df['ISO_TIME'].dt.month

# Path to your ENSO values CSV file
enso_file_path = 'HurricaneData/ENSO.txt'

# Read the ENSO values CSV file into a pandas DataFrame
enso_df = pd.read_csv(enso_file_path)

# Merge the original dataset with the ENSO dataset on Year and Month
merged_df = df.merge(enso_df, on=['Year', 'Month'], how='left')

# Display the merged DataFrame
print(merged_df.head())
