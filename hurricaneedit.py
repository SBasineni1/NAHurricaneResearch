import pandas as pd

# Read data from CSV file
df = pd.read_csv('HurricaneData/ibtracs.NA.list.v04r00.csv')

# Filter rows where 'USA_SSHS' > 1
filtered_df = df[df['USA_SSHS'] >= 1.0]

# Display the filtered DataFrame
print(filtered_df)



filtered_df.to_csv('', index=False)



