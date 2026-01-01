"""
Cleans North Atlantic IBTrACS hurricane data, removes empty columns, derives month information,
merges monthly ENSO index values by year and month, and writes the dataset back to a CSV.

Author: Suchit Basineni
Date: 7/13/24
"""

import pandas as pd
from scipy import stats
from sklearn import datasets
import seaborn as sb

file_path = 'HurricaneData/ibtracs.NA.list.v04r00.csv'
df = pd.read_csv(file_path)

print("Columns in DataFrame:", df.columns)
print(f"The number of columns in the DataFrame is: {df.shape[1]}")

df_replaced = df.replace(r'^\s*$', pd.NA, regex=True)
columns_to_drop = df_replaced.columns[df_replaced.isna().all()].tolist()
df_c = df.drop(columns=columns_to_drop)

df_c['ISO_TIME'] = pd.to_datetime(df_c['ISO_TIME'])
df_c['Month'] = df_c['ISO_TIME'].dt.strftime('%b')

if 'ISO_TIME' not in df_c.columns:
    raise KeyError("Column 'ISO_TIME' not found in the DataFrame")

enso_file_path = 'HurricaneData/ENSO.csv'
enso_df = pd.read_csv(enso_file_path)

enso_df_pivot = enso_df.melt(
    id_vars=['Year'],
    var_name='Month',
    value_name='ENSO_Value'
)

month_map = {
    'Jan': 'Jan', 'Feb': 'Feb', 'March': 'Mar', 'April': 'Apr',
    'May': 'May', 'June': 'Jun', 'July': 'Jul', 'Aug': 'Aug',
    'Sept': 'Sep', 'Oct': 'Oct', 'Nov': 'Nov', 'Dec': 'Dec'
}
enso_df_pivot['Month'] = enso_df_pivot['Month'].map(month_map)

df_c['Year'] = df_c['SEASON']

merged_df = pd.merge(
    df_c,
    enso_df_pivot,
    how='left',
    left_on=['Year', 'Month'],
    right_on=['Year', 'Month']
)

merged_df = merged_df.drop(columns=['Year'])

merged_df.to_csv(file_path, index=False)
