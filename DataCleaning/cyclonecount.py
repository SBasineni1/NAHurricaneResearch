"""
Loads North Atlantic IBTrACS hurricane track data and monthly ENSO index data, labels each storm record with an ENSO phase
(El Nino / La Nina / Neutral) based on the record date, filters to tropical storm entries, and prints counts by ENSO phase.

Author: Suchit Basineni
Date: 7/24/24
"""

import pandas as pd

hurricane_data_path = 'HurricaneData/ibtracs.NA.list.v04r00.csv'
hurricane_df = pd.read_csv(hurricane_data_path, low_memory=False)

enso_data_path = 'HurricaneData/ENSO.txt'
enso_df = pd.read_csv(enso_data_path, delim_whitespace=True, header=None, skiprows=1)

enso_header = ["Year", "Jan", "Feb", "March", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
enso_df.columns = enso_header

enso_df['Year'] = pd.to_datetime(enso_df['Year'], format='%Y')
hurricane_df['ISO_TIME'] = pd.to_datetime(hurricane_df['ISO_TIME'], errors='coerce')

def find_enso_pattern(date):
    try:
        enso_row = enso_df[enso_df['Year'].dt.year == date.year].iloc[0]
        month = date.month
        enso_value = enso_row.iloc[month]

        if enso_value > 0.5:
            return 'El Nino'
        elif enso_value < -0.5:
            return 'La Nina'
        else:
            return 'Neutral'
    except IndexError:
        return 'Unknown'

hurricane_df['ENSO'] = hurricane_df['ISO_TIME'].apply(find_enso_pattern)

hurricane_events_df = hurricane_df[hurricane_df['NATURE'] == 'TS']
hurricane_counts = hurricane_events_df['ENSO'].value_counts()
print(hurricane_counts)
