import pandas as pd

# Load the data
df = pd.read_csv('tournament_results-4-0.csv')

# Fill missing values for Rd1 Last Hole Length
df['Rd1 Last Hole Length'] = df.apply(lambda row: row['Rd2 Last Hole Length'] if pd.isna(row['Rd1 Last Hole Length']) else row['Rd1 Last Hole Length'], axis=1)
df['Rd1 Last Hole Length'] = df.apply(lambda row: row['Rd3 Last Hole Length'] if pd.isna(row['Rd1 Last Hole Length']) else row['Rd1 Last Hole Length'], axis=1)

# Fill missing values for Rd2 Last Hole Length
df['Rd2 Last Hole Length'] = df.apply(lambda row: row['Rd1 Last Hole Length'] if pd.isna(row['Rd2 Last Hole Length']) else row['Rd2 Last Hole Length'], axis=1)
df['Rd2 Last Hole Length'] = df.apply(lambda row: row['Rd3 Last Hole Length'] if pd.isna(row['Rd2 Last Hole Length']) else row['Rd2 Last Hole Length'], axis=1)

# Fill missing values for Rd3 Last Hole Length
df['Rd3 Last Hole Length'] = df.apply(lambda row: row['Rd1 Last Hole Length'] if pd.isna(row['Rd3 Last Hole Length']) else row['Rd3 Last Hole Length'], axis=1)
df['Rd3 Last Hole Length'] = df.apply(lambda row: row['Rd2 Last Hole Length'] if pd.isna(row['Rd3 Last Hole Length']) else row['Rd3 Last Hole Length'], axis=1)

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

# Save the updated data
df.to_csv('cleaned_data.csv', index=False)

