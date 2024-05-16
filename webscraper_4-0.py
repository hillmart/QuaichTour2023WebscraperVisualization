import time
start_time = time.time()

from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import csv
import re
#import concurrent.futures
from selenium.webdriver.chrome.options import Options

# Function to get last hole length using Selenium
def get_last_hole_length(url):
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(5)  

    hole_length_elements = driver.find_elements(By.CSS_SELECTOR, ".hole-length")

    if len(hole_length_elements) > 0:
        last_hole_length_str = hole_length_elements[-1].text.strip()
        
        # Remove the foot symbol (') before converting to int
        if last_hole_length_str:
            last_hole_length_int = int(last_hole_length_str[:-1])  # Using slicing
        else:
            last_hole_length_int = ''  # or some other default value
    else:
        last_hole_length_int = ''  # or some other default value

    driver.quit()
    return last_hole_length_int

# Function to scrape tournament data
def scrape_tournament(website):
    # Make a request to the website
    r = requests.get(website)

    # Parse the website with BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')

    # Get the tournament name
    h1_element = soup.find('h1')
    if h1_element:
        tournament_name = 'Event: ' + h1_element.text
    else:
        tournament_name = 'Unknown'

    # Find all the tables on the page
    tables = soup.find_all('table', class_='results')

    # Dictionary to store last hole lengths for each round and division
    last_hole_lengths = {}

    # Write the tournament name and a blank line to the CSV
    with open('tournament_data.csv', 'a', newline='') as f:
        writer = csv.writer(f)
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

                # Get last hole length for each round and division
                if division_id not in last_hole_lengths:
                    rd1_url = f"https://www.pdga.com/apps/tournament/live/event?eventId={website.split('/')[-1]}&division={division_id}&view=Scores&round=1"
                    rd2_url = f"https://www.pdga.com/apps/tournament/live/event?eventId={website.split('/')[-1]}&division={division_id}&view=Scores&round=2"
                    rd3_url = f"https://www.pdga.com/apps/tournament/live/event?eventId={website.split('/')[-1]}&division={division_id}&view=Scores&round=3"

                    rd1_last_hole_length = get_last_hole_length(rd1_url)
                    rd2_last_hole_length = get_last_hole_length(rd2_url)
                    if rd3_layout_span is not None:
                        rd3_last_hole_length = get_last_hole_length(rd3_url)
                    else:
                        rd3_last_hole_length = ''

                    last_hole_lengths[division_id] = [rd1_last_hole_length, rd2_last_hole_length, rd3_last_hole_length]

                rd1_last_hole_length, rd2_last_hole_length, rd3_last_hole_length = last_hole_lengths[division_id]

                writer.writerow([division_id, rd1_layout, rd2_layout, rd3_layout, rd1_last_hole_length, rd2_last_hole_length, rd3_last_hole_length] + data)

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
    writer.writerow(['Division ID', 'Rd1 Layout', 'Rd2 Layout', 'Rd3 Layout', 'Rd1 Last Hole Length', 'Rd2 Last Hole Length', 'Rd3 Last Hole Length', 'Place', 'Points', 'Name', 'PDGA Number', 'Rating', 'Par', 'Rd1', 'Rd2', 'Rd3', 'Rd1 Rating', 'Rd2 Rating', 'Rd3 Rating', 'Total'])

# Use multithreading to scrape the tournaments
for website in tournament_websites:
    scrape_tournament(website)

end_time = time.time()
print("Script took {} seconds to run".format(end_time - start_time))