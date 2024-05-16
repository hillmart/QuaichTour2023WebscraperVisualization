import pandas as pd
import math

# Read the CSV file
df = pd.read_csv("tournament_data.csv")

# Get the unique events in the original order
events = df['Event'].unique()

# Create a categorical column for the Event with the original order
df['Event_Order'] = pd.Categorical(df['Event'], categories=events, ordered=True)

# Set all of the rd lengths to 0 if any of the rds is 999
df.loc[(df['Rd1'] == 999) | (df['Rd2'] == 999) | (df['Rd3'] == 999), ['Rd1 Last Hole Length', 'Rd2 Last Hole Length', 'Rd3 Last Hole Length']] = 0

# Set the total to 999 if any round is 999
df.loc[(df['Rd1'] == 999) | (df['Rd2'] == 999) | (df['Rd3'] == 999), 'Total'] = 999

# Calculate the total hole length for each player
df['Total Hole Length'] = df[['Rd1 Last Hole Length', 'Rd2 Last Hole Length', 'Rd3 Last Hole Length']].sum(axis=1)

# Group by event and hole length, and find the max total for each group
max_totals = df.groupby(['Event', 'Total Hole Length'])['Total'].max()

# Sort the groups by event and total hole length in descending order
groups = max_totals.index.tolist()
groups.sort(key=lambda x: (x[0], -x[1]))

# Initialize the previous max total
previous_max_total = 0
previous_event = None

# Adjust the totals for each group
for (event, group) in groups:
    if event != previous_event:
        # Reset the previous max total when we move to a new event
        previous_max_total = 0
    if group == max([g for e, g in groups if e == event]):
        # Don't adjust the totals for the group with the largest total hole length
        df.loc[(df['Event'] == event) & (df['Total Hole Length'] == group), 'Adjusted Total'] = df.loc[(df['Event'] == event) & (df['Total Hole Length'] == group), 'Total']
    else:
        # Add the previous max total to the totals for this group
        df.loc[(df['Event'] == event) & (df['Total Hole Length'] == group), 'Adjusted Total'] = df.loc[(df['Event'] == event) & (df['Total Hole Length'] == group), 'Total'] + previous_max_total
    # Update the previous max total
    previous_max_total = max_totals[event, group]
    previous_event = event

# Finally, adjust the totals for the 999 players
df.loc[df['Total'] == 999, 'Adjusted Total'] = df.loc[df['Total'] == 999, 'Total'] + previous_max_total

# Rank normally by adjusted total within each event
df['rank'] = df.groupby('Event')['Adjusted Total'].rank(method='min', ascending=True)

# Assign the Quaich Tour Points to each player
df['Quaich Tour Points'] = df.apply(lambda row: ((1+math.floor(((df.loc[df['Event'] == row['Event']].shape[0]-row['rank'])/(df.loc[df['Event'] == row['Event']].shape[0]-1))*99))), axis=1)

# Multiply Quaich Tour Points by 1.2 if the event is a major
df['Major'] = df['Major'].astype(int)
df['Quaich Tour Points'] = df.apply(lambda row: math.floor(row['Quaich Tour Points'] * 1.2) if row['Major'] == 1 else row['Quaich Tour Points'], axis=1)

# Sort by Quatch Tour Points and Original Order
df = df.sort_values(by=['Event_Order','Quaich Tour Points'], ascending=[True, False])

# Drop unnecessary columns
df = df[['Name', 'Division ID', 'Event', 'Adjusted Total', 'rank', 'Quaich Tour Points']]

# Save to new CSV file
df.to_csv("tour_results.csv", index=False)