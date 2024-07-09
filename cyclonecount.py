import pandas as pd

# Load the hurricane data
hurricane_data_path = 'HurricaneData/ibtracs.NA.list.v04r00.csv'
hurricane_df = pd.read_csv(hurricane_data_path, low_memory=False)

# Load the ENSO data skipping the header row
enso_data_path = 'HurricaneData/ENSO.txt'
enso_df = pd.read_csv(enso_data_path, delim_whitespace=True, header=None, skiprows=1)

# Define the header for the ENSO dataset
enso_header = ["Year", "Jan", "Feb", "March", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]

# Assign header to ENSO dataset
enso_df.columns = enso_header

# Convert Year column to datetime format
enso_df['Year'] = pd.to_datetime(enso_df['Year'], format='%Y')

# Convert ISO_TIME column in hurricane_df to datetime format
hurricane_df['ISO_TIME'] = pd.to_datetime(hurricane_df['ISO_TIME'], errors='coerce')

# Function to determine ENSO pattern for a given date
def find_enso_pattern(date):
    try:
        # Find the corresponding row in enso_df
        enso_row = enso_df[enso_df['Year'].dt.year == date.year].iloc[0]

        # Determine ENSO pattern based on the value for that month
        month = date.month
        enso_value = enso_row.iloc[month]

        # Example condition, you can define your criteria for ENSO pattern
        if enso_value > 0.5:
            return 'El Nino'
        elif enso_value < -0.5:
            return 'La Nina'
        else:
            return 'Neutral'
    except IndexError:
        # Handle case where no matching row is found
        return 'Unknown'
    
# Add column for ENSO pattern to hurricane_df
hurricane_df['ENSO'] = hurricane_df['ISO_TIME'].apply(find_enso_pattern)

# Filter to include only hurricane events (assuming hurricanes are named in NAME column)
hurricane_events_df = hurricane_df[hurricane_df['NATURE'] == 'TS']

# Count the number of hurricanes in each ENSO pattern
hurricane_counts = hurricane_events_df['ENSO'].value_counts()

# Print the results
print(hurricane_counts)
