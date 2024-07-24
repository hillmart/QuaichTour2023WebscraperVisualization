<p align="center">
 <img src="https://imgur.com/5VkaeYs.png" alt="Quaich Tour Logo"></a>
</p>

<h3 align="center">Quaich Tour 2023 Webscraper Visualization</h3>

## Table of Contents
- [What is the Quaich Tour? ](#Tour_Explanation)
- [Tools and Languages](#Tools_Languages)
- [My Process](#Process)
- [How to Use It ](#Use)

## What is the Quiach Tour? <a name = "Tour_Explanation"></a>
- From the website https://www.scottishdiscgolfassociation.co.uk/quaich-tour
- The Quaich Tour is the national disc golf tour of Scotland and Ireland
- 2024 is the 10th Anniversary of the Quaich Tour
- Taking place over a year there are 17 events where players can earn tour points
- Select events are designated as Majors where players earn 1.2x points
- Players earn points for every competitor they beat at an event
- Only the top 5 point finishes for each player will count towards the final standings

I had the privilege of competing in 4 events at the end of the 2023 Quaich Tour and 5 events this year in the 2024 tour. 
Tour standings last year were posted on a spreadsheet and I was interested in visualizing the results to see how close the players 
were based on different factors such as the number of events, divisions played in, and results over time. I created these files 
so the process could be repeated on the PDGA event pages for this year's tour with minimal effort.

# Tools and Languages <a name = "Tools_Languages"></a>
- **Python**
  - **Beautiful Soup** to extract tournament results from PDGA HTML results pages
  - **Selenium Web Driver** to extract course length data from PDGA Live results pages
  - **Pandas** data manipulation for cleaning and processing results
- **Tableau** for visualizing and hosting the dashboard
  
# My Process <a name = "Process"></a>
**Webscraper**<br>
1. I started by creating the web scraper for one tournament at a time
2. Next I updated the web scraper to run on all 17 pages in one script
3. 17 pages at once ran incredibly slow so I added the multithreading library concurrent.futures
4. When I started working on the Pandas points calculation, I realized I would need course length data from the PDGA live page to differentiate divisions. Beautiful Soup
doesn't work on JS sites so I had to add selenium to get the length data for each division in each tournament
5. Final script outputs all tournaments in a single CSV with division IDs, course layout and lengths, place, name, and strokes

**Data Cleaning**<br>
I used Pandas to read the CSV and clean the data. I wrote this script iteratively with the points calculation script to make the math easier
1. I had to fill blank rounds with a score of 998 so tournaments less than 3 rounds can be run at the same time
2. Players who DNF receive scores of all 999 so they automatically get last place
3. I created a column for the event name and a boolean for major events that uses a hardcoded major list specific to the year of the tour
4. Filled in missing hole length values because tournament directors do not always put them in PDGA live
5. Finally the script removes the initial Event title lines

**Point Calculation Script**<br>
I also used Pandas to calculate the points. This script took the most work to solve the edge cases.
1. I started by calculating the points for a CSV of one tournament
2. Filtered out players with 999 so they get last place
3. Groupby on the event column and sorted by hole length
4. Used a for loop to correctly assign totals to each division
5. Implemented the spreadsheet formula using the math library
6. Used the ranking function to break ties the same way the spreadsheet did

**Tableau**<br>
Finally, I uploaded the CSV of point values to Tableau.
1. I handwrote the Matchplay event because 2024 was the last year it counted for Tour points
2. Added color coding by event
3. Added filtering by name, division, and event
4. Added filtering by the number of top events using a custom field
   
# How to Use It <a name = "Use"></a>
- Download webscraper_4-0.py, pointsCalculator_6-1.py, dataCleaner3-0.py
- Replace the 17 PDGA page links with the tournaments you want to visualize
- Run webscraper_4-0.py
- Run dataCleaner3-0.py on the result file: tournament_data.csv
- Run pointsCalculator_6-1.py on the result file of the data cleaner: cleaned_data.csv
- Upload cleaned_data.csv to Tableau and visualize
