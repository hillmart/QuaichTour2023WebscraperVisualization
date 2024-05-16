import pandas as pd
import numpy as np
import math

# Read the CSV file
df = pd.read_csv("tournament_data.csv")

# Filter out the Event line
event_lines = df[df['Division ID'].str.startswith("Event:")]
df = df[~df['Division ID'].str.startswith("Event:")]

# Calculate the total hole length for each player
df['Total Hole Length'] = df[['Rd1 Last Hole Length', 'Rd2 Last Hole Length', 'Rd3 Last Hole Length']].sum(axis=1)

# Assign the rank to each player
df['rank'] = df.groupby(['Event', 'Total Hole Length'])['Total'].rank(method='dense', ascending=False)

# Get the maximum rank for each group
max_ranks = df.groupby(['Event', 'Total Hole Length'])['rank'].max().shift().fillna(0).cumsum()

# Add the maximum rank of the previous group to the ranks of the current group
df['rank'] += df['Total Hole Length'].map(max_ranks)

# Assign the Quaitch Tour Points to each player
points_step = 100 / df.shape[0]
df['multiplier'] = df['Division ID'].apply(lambda x: 1.2 if x.startswith('Major:') else 1)
df['Quaich Tour Points'] = df.apply(lambda row: int(round((1+math.floor(((row['rank']-1)/((df['Name'].count()-1))*99))*row['multiplier']),0)), axis=1)

# Drop unnecessary columns
df = df[['Name', 'Division ID', 'Total', 'Quaich Tour Points']]

# Sort by Quatch Tour Points
df = df.sort_values(by='Quaich Tour Points', ascending=False)

# Save to new CSV file
with open("tour_results.csv", "w") as f:
    f.write(",".join(df.columns) + "\n")
    event_lines_str = event_lines.to_csv(header=False, index=False)
    f.write(event_lines_str)
    df.to_csv(f, header=False, index=False)