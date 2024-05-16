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
max_totals = df.groupby('Total Hole Length')['Total'].max().cumsum().shift(1).fillna(0)

# Sort max_totals in descending order of the index
max_totals = max_totals.sort_values(ascending=False)

# Add the max total of the previous group to the total for every player in the next group
df['Adjusted Total'] = df['Total'] + df['Total Hole Length'].map(max_totals)

# Rank normally by adjusted total
df['rank'] = df['Adjusted Total'].rank(method='min', ascending=True)

# Assign the Quaich Tour Points to each player
total_players = df.shape[0]
df['Quaich Tour Points'] = df.apply(lambda row: int(round((1+math.floor(((total_players-row['rank'])/(total_players-1))*99)),0)), axis=1)

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



# import pandas as pd
# import math

# # Read the CSV file
# df = pd.read_csv("tournament_data.csv")

# # Set all round lengths to 0 if any round is 999
# df.loc[(df['Rd1'] == 999) | (df['Rd2'] == 999) | (df['Rd3'] == 999), ['Rd1 Last Hole Length', 'Rd2 Last Hole Length', 'Rd3 Last Hole Length']] = 0

# # Calculate the total hole length for each player
# df['Total Hole Length'] = df[['Rd1 Last Hole Length', 'Rd2 Last Hole Length', 'Rd3 Last Hole Length']].sum(axis=1)

# # Set total to 999 if any round is 999
# df.loc[(df['Rd1'] == 999) | (df['Rd2'] == 999) | (df['Rd3'] == 999), ['Total']] = 999

# # Assign the rank to each player
# df['rank'] = df.groupby('Total Hole Length')['Total'].rank(method='max', ascending=False)

# # Get the maximum rank for each group
# max_ranks = df.groupby('Total Hole Length')['rank'].max().shift(1).cumsum().fillna(0)

# # Add the maximum rank of the previous group to the ranks of the current group
# df['rank'] += df['Total Hole Length'].map(max_ranks)

# # Invert the ranks
# df['rank'] = df['rank'].max() - df['rank'] + 1

# # Assign the Quaich Tour Points to each player
# total_players = df.shape[0]
# df['Quaich Tour Points'] = df.apply(lambda row: int(round((1+math.floor(((total_players-row['rank'])/(total_players-1))*99)),0)), axis=1)

# # Drop unnecessary columns
# df = df[['Name', 'Division ID', 'Total', 'rank', 'Quaich Tour Points']]

# # Sort by Quatch Tour Points
# df = df.sort_values(by='Quaich Tour Points', ascending=False)

# # Save to new CSV file
# with open("tour_results.csv", "w") as f:
#     f.write(",".join(df.columns) + "\n")
#     df.to_csv(f, header=False, index=False)


# import pandas as pd
# import math

# # Read the CSV file
# df = pd.read_csv("tournament_data.csv")

# # Calculate the total hole length for each player
# df['Total Hole Length'] = df[['Rd1 Last Hole Length', 'Rd2 Last Hole Length', 'Rd3 Last Hole Length']].sum(axis=1)

# # Assign the rank to each player
# df['rank'] = df.groupby('Total Hole Length')['Total'].rank(method='max', ascending=False)

# # Get the maximum rank for each group
# max_ranks = df.groupby('Total Hole Length')['rank'].max().shift(1).cumsum().fillna(0)

# # Add the maximum rank of the previous group to the ranks of the current group
# df['rank'] += df['Total Hole Length'].map(max_ranks)

# # Invert the ranks
# df['rank'] = df['rank'].max() - df['rank'] + 1

# # Assign the Quaich Tour Points to each player
# total_players = df.shape[0]
# df['Quaich Tour Points'] = df.apply(lambda row: int(round((1+math.floor(((total_players-row['rank'])/(total_players-1))*99)),0)), axis=1)

# # Drop unnecessary columns
# df = df[['Name', 'Division ID', 'Total', 'rank', 'Quaich Tour Points']]

# # Sort by Quatch Tour Points
# df = df.sort_values(by='Quaich Tour Points', ascending=False)

# # Save to new CSV file
# with open("tour_results.csv", "w") as f:
#     f.write(",".join(df.columns) + "\n")
#     df.to_csv(f, header=False, index=False)