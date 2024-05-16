import pandas as pd

# Load the data
df = pd.read_csv('tournament_data.csv')

# Fill missing values for Rd1 Last Hole Length
df['Rd1 Last Hole Length'] = df.apply(lambda row: row['Rd2 Last Hole Length'] if pd.isna(row['Rd1 Last Hole Length']) else row['Rd1 Last Hole Length'], axis=1)
df['Rd1 Last Hole Length'] = df.apply(lambda row: row['Rd3 Last Hole Length'] if pd.isna(row['Rd1 Last Hole Length']) else row['Rd1 Last Hole Length'], axis=1)

# Fill missing values for Rd2 Last Hole Length
df['Rd2 Last Hole Length'] = df.apply(lambda row: row['Rd1 Last Hole Length'] if pd.isna(row['Rd2 Last Hole Length']) else row['Rd2 Last Hole Length'], axis=1)
df['Rd2 Last Hole Length'] = df.apply(lambda row: row['Rd3 Last Hole Length'] if pd.isna(row['Rd2 Last Hole Length']) else row['Rd2 Last Hole Length'], axis=1)

# Fill missing values for Rd3 Last Hole Length
df['Rd3 Last Hole Length'] = df.apply(lambda row: row['Rd1 Last Hole Length'] if pd.isna(row['Rd3 Last Hole Length']) else row['Rd3 Last Hole Length'], axis=1)
df['Rd3 Last Hole Length'] = df.apply(lambda row: row['Rd2 Last Hole Length'] if pd.isna(row['Rd3 Last Hole Length']) else row['Rd3 Last Hole Length'], axis=1)

# Create a new column for event
df['Event'] = df['Division ID'].apply(lambda x: x if 'Event:' in x or 'Major:' in x else None)

# Fill in the missing values in the 'Event' column
df['Event'] = df['Event'].fillna(method='bfill')

# Create a new column for major
df['Major'] = df['Division ID'].apply(lambda x: 1 if 'Major:' in x else 0)

# Fill in the missing values in the 'Major' column
df['Major'] = df['Major'].fillna(method='bfill')
# Save the updated data
df.to_csv('cleaned_data.csv', index=False)