from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL of OECD BEPS MLI Matching Database
url = "https://www.oecd.org/en/data/tools/beps-mli-matching-database.html"

# Open the page
driver.get(url)
time.sleep(5)  # Wait for JavaScript to load content

# Locate table and extract rows
table_rows = driver.find_elements(By.TAG_NAME, "tr")
data = []

# Extract text from each row
for row in table_rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    if cols:
        data.append([col.text for col in cols])

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV or display
df.to_csv("oecd_data.csv", index=False)
print(df.head())  # Display first few rows

# Close driver
driver.quit()
