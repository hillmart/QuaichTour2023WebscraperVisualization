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

# Filter out players with a total of 999 and a hole length of 0
df_filtered = df[(df['Total'] != 999) | (df['Total Hole Length'] != 0)]
# Group by hole length and rank players within each group
df_filtered['rank'] = df_filtered.groupby('Total Hole Length')['Total'].rank(method='min', ascending=True)

# Adjust the rank to account for the groupings
df_filtered['rank'] = df_filtered['rank'] + df_filtered['Total Hole Length'].rank(method='min', ascending=False) - 1

# Fill NaN values in the 'rank' column with the total number of players
df_filtered['rank'] = df_filtered['rank'].fillna(df_filtered['rank'].max() + 1)

# Assign the remaining players (those with a total of 999) to the last place
df.loc[~df.index.isin(df_filtered.index), 'rank'] = df_filtered['rank'].max() + 1

# Assign the Quaich Tour Points to each player
total_players = df.shape[0]
df['Quaich Tour Points'] = df.apply(lambda row: int(math.floor((1+math.floor(((total_players-row['rank'])/(total_players-1))*99)) * (1.2 if row['Major'] == 1 else 1))), axis=1)

# Drop unnecessary columns
df = df[['Name', 'Division ID', 'Total', 'rank', 'Quaich Tour Points']]

# Sort by Quatch Tour Points
df = df.sort_values(by='Quaich Tour Points', ascending=False)

# Save to new CSV file
with open("tour_results.csv", "w") as f:
    f.write(",".join(df.columns) + "\n")
    df.to_csv(f, header=False, index=False)

# # # Group by hole length and find the max total for each group
# # max_totals = df_filtered.groupby('Total Hole Length')['Total'].max().cumsum().shift(1).fillna(0)

# # # Sort max_totals in descending order of the index
# # max_totals = max_totals.sort_index(ascending=False)

# # # Add the max total of the previous group to the total for every player in the next group
# # df['Adjusted Total'] = df['Total'] + df['Total Hole Length'].map(max_totals)

# # # Rank normally by adjusted total
# # df['rank'] = df['Adjusted Total'].rank(method='min', ascending=True)

# # # Fill NaN values in the 'rank' column with the total number of players
# # df['rank'] = df['rank'].fillna(df['rank'].max() + 1)

# # Group by hole length and rank players within each group
# df['rank'] = df.groupby('Total Hole Length')['Total'].rank(method='min', ascending=True)

# # Adjust the rank to account for the groupings
# df['rank'] = df['rank'] + df['Total Hole Length'].rank(method='min', ascending=False) - 1

# # Fill NaN values in the 'rank' column with the total number of players
# df['rank'] = df['rank'].fillna(df['rank'].max() + 1)


# # Assign the Quaich Tour Points to each player
# total_players = df.shape[0]
# df['Quaich Tour Points'] = df.apply(lambda row: int(math.floor((1+math.floor(((total_players-row['rank'])/(total_players-1))*99)) * (1.2 if row['Major'] == 1 else 1))), axis=1)

# # Drop unnecessary columns
# df = df[['Name', 'Division ID', 'Total', 'rank', 'Quaich Tour Points']]

# # Sort by Quatch Tour Points
# df = df.sort_values(by='Quaich Tour Points', ascending=False)

# # Save to new CSV file
# with open("tour_results.csv", "w") as f:
#     f.write(",".join(df.columns) + "\n")
#     df.to_csv(f, header=False, index=False)