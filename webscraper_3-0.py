import requests
from bs4 import BeautifulSoup
import csv
import re
import threading

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
with open('tournament_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(['Division ID', 'Rd1 Layout', 'Rd2 Layout', 'Rd3 Layout', 'Place', 'Points', 'Name', 'PDGA Number', 'Rating', 'Par', 'Rd1', 'Rd2', 'Rd3', 'Rd1 Rating', 'Rd2 Rating', 'Rd3 Rating', 'Total'])

    def scrape_tournament(website):
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
                data = [''] * 13  # Initialize data with 16 empty strings
                columns = row.find_all('td')
                for column in columns:
                    if 'place' in column.get('class'):
                        data[0] = column.text
                    elif 'points' in column.get('class'):
                        data[1] = column.text
                    elif 'player' in column.get('class'):
                        data[2] = column.text
                    elif 'pdga-number' in column.get('class'):
                        data[3] = column.text
                    elif 'player-rating' in column.get('class'):
                        data[4] = column.text
                    elif 'par' in column.get('class'):
                        data[5] = column.text
                    elif 'round' in column.get('class'):
                        for i in range(6, 9):
                            if data[i] == '':
                                data[i] = column.text
                                break
                    elif 'round-rating' in column.get('class'):
                        for i in range(9, 12):
                            if data[i] == '':
                                data[i] = column.text
                                break
                    elif 'total' in column.get('class'):
                        data[12] = column.text
                        if data[12] == 'DNF':
                            data[12] = '999'

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

                writer.writerow([division_id] + [rd1_layout, rd2_layout, rd3_layout] + data)

    threads = []
    for website in tournament_websites:
        thread = threading.Thread(target=scrape_tournament, args=(website,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()