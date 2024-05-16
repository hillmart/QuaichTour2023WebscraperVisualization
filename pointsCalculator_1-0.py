import pandas as pd
import math

# Read the CSV file
df = pd.read_csv("tournament_data.csv")

# Filter out the Event line
event_line = df[df['Division ID'].str.startswith("Event:")]
df = df[~df['Division ID'].str.startswith("Event:")]

# Drop rows with missing values
#df = df.dropna()

# Calculate the rank and Quaitch Tour Points
df['rank'] = df['Total'].rank(ascending=True, method='min')
points_step = 100 / df.shape[0]
df['multiplier'] = df['Division ID'].apply(lambda x: 1.2 if x.startswith('Major:') else 1)
df['Quaitch Tour Points'] = df.apply(lambda row: int(round((1+math.floor(((df['Name'].count()-row['rank'])/((df['Name'].count()-1))*99))*row['multiplier']),0)), axis=1)

# Drop unnecessary columns
df = df[['Name', 'Division ID', 'Total', 'rank', 'Quaitch Tour Points']]

# Sort by Quatch Tour Points
df = df.sort_values(by='Quaitch Tour Points', ascending=False)

# Save to new CSV file
with open("tour_results.csv", "w") as f:
    f.write(",".join(df.columns) + "\n")
    event_line = event_line.dropna(axis=1)
    event_line_str = event_line.to_csv(header=False, index=False)
    f.write(event_line_str)
    df.to_csv(f, header=False, index=False)