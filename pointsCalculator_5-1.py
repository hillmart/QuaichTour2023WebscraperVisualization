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

# Group by hole length and find the max total for each group
max_totals = df.groupby('Total Hole Length')['Total'].max()

# Sort the groups by total hole length in descending order
groups = max_totals.index.tolist()
groups.sort(reverse=True)

# Initialize the previous max total
previous_max_total = 0

# Adjust the totals for each group
for group in groups:
    if group == max(groups):
        # Don't adjust the totals for the group with the largest total hole length
        df.loc[df['Total Hole Length'] == group, 'Adjusted Total'] = df.loc[df['Total Hole Length'] == group, 'Total']
    else:
        # Add the previous max total to the totals for this group
        df.loc[df['Total Hole Length'] == group, 'Adjusted Total'] = df.loc[df['Total Hole Length'] == group, 'Total'] + previous_max_total
    # Update the previous max total
    previous_max_total = max_totals[group]

# Finally, adjust the totals for the 999 players
df.loc[df['Total'] == 999, 'Adjusted Total'] = df.loc[df['Total'] == 999, 'Total'] + previous_max_total

# Rank normally by adjusted total
df['rank'] = df['Adjusted Total'].rank(method='min', ascending=True)

# Assign the Quaich Tour Points to each player
total_players = df.shape[0]
df['Quaich Tour Points'] = df.apply(lambda row: int(round((1+math.floor(((total_players-row['rank'])/(total_players-1))*99)),0)) if row['Total'] != 999 else 0, axis=1)

# Multiply Quaich Tour Points by 1.2 if the event is a major
df.loc[df['Major'] == '1', 'Quaich Tour Points'] *= 1.2

# Drop unnecessary columns
df = df[['Name', 'Division ID', 'Adjusted Total', 'rank', 'Quaich Tour Points']]

# Sort by Quatch Tour Points
df = df.sort_values(by='Quaich Tour Points', ascending=False)

# Save to new CSV file
with open("tour_results.csv", "w") as f:
    f.write(",".join(df.columns) + "\n")
    df.to_csv(f, header=False, index=False)