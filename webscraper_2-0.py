import requests
from bs4 import BeautifulSoup
import csv
import re

# List of tournament websites
tournament_websites = [
    "https://www.pdga.com/tour/event/66904",
    "https://www.pdga.com/tour/event/67963",
    "https://www.pdga.com/tour/event/67568",
    "https://www.pdga.com/tour/event/69004",
    "https://www.pdga.com/tour/event/69013",
    "https://www.pdga.com/tour/event/69437",
    "https://www.pdga.com/tour/event/69985",
    "https://www.pdga.com/tour/event/71269",
    "https://www.pdga.com/tour/event/64654",
    "https://www.pdga.com/tour/event/72693",
    "https://www.pdga.com/tour/event/72457",
    "https://www.pdga.com/tour/event/72701",
    "https://www.pdga.com/tour/event/71628",
    "https://www.pdga.com/tour/event/73200",
    "https://www.pdga.com/tour/event/73382",
    "https://www.pdga.com/tour/event/72821",
    "https://www.pdga.com/tour/event/74595",
]

# Create a CSV file to write to
with open('tournament_results-2-0.csv', 'w', newline='') as f:
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(['Division ID', 'Place', 'Points', 'Name', 'PDGA Number', 'Rating', 'Par', 'Rd1', 'Rd1 Rating', 'Rd1 Layout', 'Rd2', 'Rd2 Rating', 'Rd2 Layout', 'Rd3', 'Rd3 Rating', 'Rd3 Layout', 'Total'])

    # Loop through each tournament website
    for website in tournament_websites:
        # Make a request to the website
        r = requests.get(website)

        # Parse the website with BeautifulSoup
        soup = BeautifulSoup(r.text, 'html.parser')

        # Get the tournament name
        tournament_name = 'Event: ' + soup.find('h1').text

        # Find all the tables on the page
        tables = soup.find_all('table', class_='results')

        # Write the tournament name and a blank line to the CSV
        writer.writerow([])
        writer.writerow([tournament_name])

        # Loop through each table
        for table in tables:
            division_id = table.find_previous('h3').get('id')
            # Write the data rows
            for row in table.find_all('tr')[1:]:  # Skip the header row
                data = [''] * 13  # Initialize data with 13 empty strings
                columns = row.find_all('td')
                for i, column in enumerate(columns):
                    try:
                        data[i] = column.text
                    except IndexError:
                        pass  # Do nothing if the index is out of range
                place = data[0]
                points = data[1]
                name = data[2]
                pdga_number = data[3]
                rating = data[4]
                par = data[5]
                rd1 = data[6]
                rd1_rating = data[7]
                rd2 = data[8]
                rd2_rating = data[9]
                rd3 = data[10]
                rd3_rating = data[11]
                total = data[12]

                # Find the layout details for each round
                rd1_layout_span = soup.find('span', id=re.compile('^layout-details-'+website.split('/')[-1]+'-'+division_id+'-round-Rd1$'))
                if rd1_layout_span is not None:
                    rd1_layout = re.search(r'Par (\d+)', rd1_layout_span.text).group(1)
                else:
                    rd1_layout = ''
                rd2_layout_span = soup.find('span', id=re.compile('^layout-details-'+website.split('/')[-1]+'-'+division_id+'-round-Rd2$'))
                if rd2_layout_span is not None:
                    rd2_layout = re.search(r'Par (\d+)', rd2_layout_span.text).group(1)
                else:
                    rd2_layout = ''
                rd3_layout_span = soup.find('span', id=re.compile('^layout-details-'+website.split('/')[-1]+'-'+division_id+'-round-Rd3$'))
                if rd3_layout_span is not None:
                    rd3_layout = re.search(r'Par (\d+)', rd3_layout_span.text).group(1)
                else:
                    rd3_layout = ''

                writer.writerow([division_id, place, points, name, pdga_number, rating, par, rd1, rd1_rating, rd1_layout, rd2, rd2_rating, rd2_layout, rd3, rd3_rating, rd3_layout, total])