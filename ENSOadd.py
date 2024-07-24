import scipy
from scipy import stats
from sklearn import datasets
import pandas as pd
import seaborn as sb
# import numpy as np
#import os

# Path to your CSV file
file_path = 'HurricaneData/ibtracs.NA.list.v04r00.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# Display the columns to verify the column names
print("Columns in DataFrame:", df.columns)
num_columns = df.shape[1]
print(f"The number of columns in the DataFrame is: {num_columns}")


#The data frame has several columns with empty space '  ' as values . 
# Thhese empty columns are dropped and now our data frame has 59 columns


# Replace spaces and empty strings with NaN
df_replaced = df.replace(r'^\s*$', pd.NA, regex=True)

# Identify columns with all NaN values after replacement
columns_to_drop = df_replaced.columns[df_replaced.isna().all()].tolist()

# Drop identified columns
df_c = df.drop(columns=columns_to_drop)

print("Cleaned DataFrame:")
print(df_c)

# Convert 'ISO_TIME' column to datetime format
df_c['ISO_TIME'] = pd.to_datetime(df_c['ISO_TIME'])

# Add a new column 'Month' with month abbreviation (e.g., Jan, Feb)
df_c['Month'] = df_c['ISO_TIME'].dt.strftime('%b')

print(df_c)



# Ensure 'ISO_TIME' column is present
if 'ISO_TIME' not in df_c.columns:
    raise KeyError("Column 'ISO_TIME' not found in the DataFrame")



# Path to your ENSO values CSV file
enso_file_path = 'HurricaneData/ENSO.csv'

# Read the ENSO values CSV file into a pandas DataFrame
enso_df = pd.read_csv(enso_file_path)

# Melt the first data frame to long format
enso_df_pivot = enso_df.melt(id_vars=['Year'], var_name='Month', value_name='ENSO_Value')

# Since Month names are not standard in the ENSO dataframe the months have to renamed or remapped.
month_map = {'Jan': 'Jan', 'Feb': 'Feb', 'March': 'Mar','April': 'Apr', 'May': 'May', 'June': 'Jun','July': 'Jul', 'Aug': 'Aug', 'Sept': 'Sep','Oct': 'Oct', 'Nov': 'Nov', 'Dec': 'Dec'}
enso_df_pivot['Month'] = enso_df_pivot['Month'].map(month_map)



df_c['Year'] = df_c['SEASON']

# Merge the data frames on Year and Month
merged_df = pd.merge(df_c, enso_df_pivot, how='left', left_on=['Year', 'Month'], right_on=['Year', 'Month'])

# Drop the extra Year column if needed
merged_df = merged_df.drop(columns=['Year'])

print(merged_df)

merged_df.to_csv(file_path, index=False)


