import requests
from bs4 import BeautifulSoup
import csv

# URL of the Nominatim Country Codes page
url = 'https://wiki.openstreetmap.org/wiki/Nominatim/Country_Codes'

# Send a GET request to the page
response = requests.get(url)
response.raise_for_status()  # Raise an exception for HTTP errors

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find the first table on the page (which contains the country codes)
table = soup.find('table')

# Initialize a list to store the extracted data
country_data = []

# Iterate over the rows of the table
for row in table.find_all('tr')[1:]:  # Skip the header row
    cols = row.find_all('td')
    if len(cols) >= 2:
        country_name = cols[1].get_text(strip=True)
        country_data.append([country_name])

# Write the data to a CSV file
with open('nominatim_country_codes.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Country Name'])
    writer.writerows(country_data)

print("CSV file 'nominatim_country_codes.csv' has been created.")
