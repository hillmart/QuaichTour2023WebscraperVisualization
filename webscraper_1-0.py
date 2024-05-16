import requests
from bs4 import BeautifulSoup
import csv
import re

# Make a request to the website
r = requests.get("https://www.pdga.com/tour/event/72821#MA1")

# Parse the website with BeautifulSoup
soup = BeautifulSoup(r.text, 'html.parser')

# Find all the tables on the page
tables = soup.find_all('table', class_='results')

# Create a CSV file to write to
with open('tournament_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(['Division ID', 'Place', 'Points', 'Name', 'PDGA Number', 'Rating', 'Par', 'Rd1', 'Rd1 Rating', 'Rd1 Layout', 'Rd2', 'Rd2 Rating', 'Rd2 Layout', 'Rd3', 'Rd3 Rating', 'Rd3 Layout', 'Total'])

    # Loop through each table
    for table in tables:
        division_id = table.find_previous('h3').get('id')
        # Write the data rows
        for row in table.find_all('tr')[1:]:  # Skip the header row
            data = row.find_all('td')
            place = data[0].text
            points = data[1].text
            name = data[2].text
            pdga_number = data[3].text
            rating = data[4].text
            par = data[5].text
            rd1 = data[6].text
            rd1_rating = data[7].text
            rd2 = data[8].text
            rd2_rating = data[9].text
            rd3 = data[10].text
            rd3_rating = data[11].text
            total = data[12].text

            # Find the layout details for each round
            rd1_layout_span = soup.find('span', id=re.compile('^layout-details-72821-'+division_id+'-round-Rd1$'))
            if rd1_layout_span is not None:
                rd1_layout = rd1_layout_span.text.split('Par')[1].split(';')[0].strip()
            else:
                rd1_layout = ''
            rd2_layout_span = soup.find('span', id=re.compile('^layout-details-72821-'+division_id+'-round-Rd2$'))
            if rd2_layout_span is not None:
                rd2_layout = rd2_layout_span.text.split('Par')[1].split(';')[0].strip()
            else:
                rd2_layout = ''
            rd3_layout_span = soup.find('span', id=re.compile('^layout-details-72821-'+division_id+'-round-Rd3$'))
            if rd3_layout_span is not None:
                rd3_layout = rd3_layout_span.text.split('Par')[1].split(';')[0].strip()
            else:
                rd3_layout = ''

            writer.writerow([division_id, place, points, name, pdga_number, rating, par, rd1, rd1_rating, rd1_layout, rd2, rd2_rating, rd2_layout, rd3, rd3_rating, rd3_layout, total])