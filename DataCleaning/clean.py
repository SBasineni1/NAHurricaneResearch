"""
Preprocessing the North Atlantic IBTrACS dataset by ensuring valid season values
and restricting the data to 1950–2024.

Author: Suchit Basineni
Date: 7/9/24
"""

import pandas as pd

df = pd.read_csv('HurricaneData/ibtracs.NA.list.v04r00.csv')
df['SEASON'] = pd.to_numeric(df['SEASON'], errors='coerce')
df = df.dropna(subset=['SEASON'])
df['SEASON'] = df['SEASON'].astype(int)
df_filtered = df[(df['SEASON'] >= 1950) & (df['SEASON'] <= 2024)]
df_filtered.to_csv('HurricaneData/ibtracs.NA.list.v04r00.csv', index=False)

