import pandas as pd

# Load the data
df = pd.read_csv('tournament_results-2-0.csv')

# Fill missing values for Rd1, Rd2, Rd3 with 998 where RdX Layout is NaN
df.loc[df['Rd1 Layout'].isna(), 'Rd1'] = 998
df.loc[df['Rd2 Layout'].isna(), 'Rd2'] = 998
df.loc[df['Rd3 Layout'].isna(), 'Rd3'] = 998

# Fill any remaining missing values for Rd1, Rd2, Rd3 with 999
df['Rd1'] = df['Rd1'].fillna(999)
df['Rd2'] = df['Rd2'].fillna(999)
df['Rd3'] = df['Rd3'].fillna(999)

# Create a new column for event and major
df['Event'] = None
df['Major'] = 0

# Initialize the current event and major
current_event = None
current_major = 0

# Iterate over the rows in the dataframe
for index, row in df.iterrows():
    # If the Division ID contains 'Event:', update the current event and major
    if 'Event:' in row['Division ID']:
        current_event = row['Division ID'].replace('Event: ', '')
        current_major = 0
    # If the Division ID contains 'Major:', update the current event and major
    elif 'Major:' in row['Division ID']:
        current_event = row['Division ID'].replace('Major: ', '')
        current_major = 1
    
    # Update the Event and Major columns for the current row
    df.loc[index, 'Event'] = current_event
    df.loc[index, 'Major'] = current_major


# Fill missing values for Rd1 Last Hole Length
min_hole_length = df[['Rd1 Last Hole Length', 'Rd2 Last Hole Length', 'Rd3 Last Hole Length']].min(axis = 1, skipna=True)
df['Rd1 Last Hole Length'] = df['Rd1 Last Hole Length'].fillna(min_hole_length)

# Fill missing values for Rd2 Last Hole Length
df['Rd2 Last Hole Length'] = df['Rd2 Last Hole Length'].fillna(min_hole_length)

# Fill missing values for Rd3 Last Hole Length
df['Rd3 Last Hole Length'] = df['Rd3 Last Hole Length'].fillna(min_hole_length)

# Remove rows where Division ID contains 'Event:' or 'Major:'
df = df[~df['Division ID'].str.contains('Event:|Major:')]

# Save the updated data
df.to_csv('cleaned_data.csv', index=False)