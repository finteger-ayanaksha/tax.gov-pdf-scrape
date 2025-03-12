import pandas as pd
from bs4 import BeautifulSoup

# Load the HTML content
with open('data.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Initialize lists to store the data
countries = []
dates1 = []
dates2 = []
dates3 = []
statuses = []
extra1 = []
extra2 = []
extra3 = []
extra4 = []
extra5 = []

# Find all rows in the table
rows = soup.find_all('div', {'role': 'row'})

for row in rows:
    # Extract country name
    country = row.find('div', {'role': 'rowheader'})
    if country:
        countries.append(country.text.strip())
    
    # Extract other data cells
    cells = row.find_all('div', {'role': 'gridcell'})
    if cells:
        dates1.append(cells[0].text.strip())
        dates2.append(cells[1].text.strip())
        dates3.append(cells[2].text.strip())
        statuses.append(cells[3].text.strip())
        extra1.append(cells[4].text.strip())
        extra2.append(cells[5].text.strip())
        extra3.append(cells[6].text.strip())
        extra4.append(cells[7].text.strip())
        extra5.append(cells[8].text.strip())

# Create a DataFrame
data = {
    'Country': countries,
    'Date1': dates1,
    'Date2': dates2,
    'Date3': dates3,
    'Status': statuses,
    'Extra1': extra1,
    'Extra2': extra2,
    'Extra3': extra3,
    'Extra4': extra4,
    'Extra5': extra5
}

df = pd.DataFrame(data)

# Save to CSV
df.to_csv('output.csv', index=False)