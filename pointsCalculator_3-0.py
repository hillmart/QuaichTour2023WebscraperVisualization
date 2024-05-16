import pandas as pd
import numpy as np
import math

# Read the CSV file
df = pd.read_csv("tournament_data.csv")

# Split the data into separate events
events = df[df['Division ID'].str.startswith("Event:")]
events = events.index.tolist()
events.append(len(df))

# Process each event separately
event_results = []
for i in range(len(events) - 1):
    event_df = df.iloc[events[i]+1:events[i+1]]
    
    # Calculate the total hole length for each player
    event_df['Total Hole Length'] = event_df[['Rd1 Last Hole Length', 'Rd2 Last Hole Length', 'Rd3 Last Hole Length']].sum(axis=1)

    # Assign the rank to each player
    event_df['rank'] = event_df.groupby('Total Hole Length')['Total'].rank(method='dense', ascending=False)

    # Get the maximum rank for each group
    max_ranks = event_df.groupby('Total Hole Length')['rank'].max().shift().fillna(0).cumsum()

    # Add the maximum rank of the previous group to the ranks of the current group
    event_df['rank'] += event_df['Total Hole Length'].map(max_ranks)

    # Assign the Quaitch Tour Points to each player
    points_step = 100 / event_df.shape[0]
    event_df['multiplier'] = event_df['Division ID'].apply(lambda x: 1.2 if x.startswith('Major:') else 1)
    event_df['Quaich Tour Points'] = event_df.apply(lambda row: int(round((1+math.floor(((row['rank']-1)/((event_df['Name'].count()-1))*99))*row['multiplier']),0)), axis=1)

    # Drop unnecessary columns
    event_df = event_df[['Name', 'Division ID', 'Total', 'Quaich Tour Points']]

    # Sort by Quatch Tour Points
    event_df = event_df.sort_values(by='Quaich Tour Points', ascending=False)

    # Append the results to the list
    event_results.append(event_df)

# Save to new CSV file
with open("tour_results.csv", "w") as f:
    for event in event_results:
        event.to_csv(f, header=True, index=False)
        f.write("\n")