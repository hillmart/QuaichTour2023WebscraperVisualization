import pandas as pd
import math

# Read the CSV file
df = pd.read_csv("tournament_data.csv")

# Set all of the rd lengths to 0 if any of the rds is 999
df.loc[(df['Rd1'] == 999) | (df['Rd2'] == 999) | (df['Rd3'] == 999), ['Rd1 Last Hole Length', 'Rd2 Last Hole Length', 'Rd3 Last Hole Length']] = 0

# Set the total to 999 if any round is 999
df.loc[(df['Rd1'] == 999) | (df['Rd2'] == 999) | (df['Rd3'] == 999), 'Total'] = 999

# Calculate the total hole length for each player
df['Total Hole Length'] = df[['Rd1 Last Hole Length', 'Rd2 Last Hole Length', 'Rd3 Last Hole Length']].sum(axis=1)

# Group by Event ID and Total Hole Length, and find the max total for each group
max_totals = df.groupby(['Event', 'Total Hole Length'])['Total'].max()

# Sort the groups by Event ID and total hole length in descending order
groups = max_totals.index.tolist()
groups.sort(key=lambda x: (x[0], -x[1]))

# Initialize the previous max total
previous_max_total = 0
previous_event_id = None

# Adjust the totals for each group
for event_id, group in groups:
    if event_id != previous_event_id:
        # Reset the previous max total when a new event starts
        previous_max_total = 0
    if group == max([g for e, g in groups if e == event_id]):
        # Don't adjust the totals for the group with the largest total hole length
        df.loc[(df['Event'] == event_id) & (df['Total Hole Length'] == group), 'Adjusted Total'] = df.loc[(df['Event'] == event_id) & (df['Total Hole Length'] == group), 'Total']
    else:
        # Add the previous max total to the totals for this group
        df.loc[(df['Event'] == event_id) & (df['Total Hole Length'] == group), 'Adjusted Total'] = df.loc[(df['Event'] == event_id) & (df['Total Hole Length'] == group), 'Total'] + previous_max_total
    # Update the previous max total
    previous_max_total = max_totals[event_id, group]
    previous_event_id = event_id

# Finally, adjust the totals for the 999 players
df.loc[df['Total'] == 999, 'Adjusted Total'] = df.loc[df['Total'] == 999, 'Total'] + previous_max_total

# Rank normally by adjusted total within each event
df['rank'] = df.groupby('Event')['Adjusted Total'].rank(method='min', ascending=True)

# Assign the Quaich Tour Points to each player
df['Quaich Tour Points'] = df.groupby('Event').apply(lambda x: ((1+((x.shape[0]-x['rank'])/(x.shape[0]-1))*99).apply(math.floor))).reset_index(level=0, drop=True)

# Multiply Quaich Tour Points by 1.2 if the event is a major
df['Major'] = df['Major'].astype(int)
df['Quaich Tour Points'] = df.apply(lambda row: math.floor(row['Quaich Tour Points'] * 1.2) if row['Major'] == 1 else row['Quaich Tour Points'], axis=1)

# Drop unnecessary columns
df = df[['Name', 'Division ID', 'Adjusted Total', 'rank', 'Quaich Tour Points', 'Event']]

# Sort by Quatch Tour Points
df = df.sort_values(by=['Event', 'Quaich Tour Points'], ascending=[True, False])

# Save to new CSV file
with open("tour_results.csv", "w") as f:
    f.write(",".join(df.columns) + "\n")
    df.to_csv(f, header=False, index=False)