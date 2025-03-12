import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup Selenium WebDriver
options = Options()
options.headless = False  # Set to True to run in headless mode
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Open the OECD BEPS MLI Matching Database page
url = "https://www.oecd.org/en/data/tools/beps-mli-matching-database.html"
driver.get(url)

# Wait for the Power BI table to load (increase time if needed)
wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='row']")))

# Get page source and parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Close the browser after extracting the content
driver.quit()

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
    if len(cells) >= 9:  # Ensure there are enough columns
        dates1.append(cells[0].text.strip())
        dates2.append(cells[1].text.strip())
        dates3.append(cells[2].text.strip())
        statuses.append(cells[3].text.strip())
        extra1.append(cells[4].text.strip())
        extra2.append(cells[5].text.strip())
        extra3.append(cells[6].text.strip())
        extra4.append(cells[7].text.strip())
        extra5.append(cells[8].text.strip())
    else:
        # Fill missing data with empty strings if columns are missing
        dates1.append("")
        dates2.append("")
        dates3.append("")
        statuses.append("")
        extra1.append("")
        extra2.append("")
        extra3.append("")
        extra4.append("")
        extra5.append("")

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
df.to_csv('oecd_beps_mli_data.csv', index=False)

print("Data saved successfully to 'oecd_beps_mli_data.csv'")
