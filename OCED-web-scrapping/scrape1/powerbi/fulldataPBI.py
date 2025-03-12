import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup Selenium WebDriver
options = Options()
options.headless = False  # Set to True to run in the background
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Open the Power BI dashboard
url = "https://app.powerbi.com/view?r=eyJrIjoiYmQ5NGE3M2EtNTdhZi00NTFkLTkxNzEtNzQzMWU0NjBmYTI5IiwidCI6ImFjNDFjN2Q0LTFmNjEtNDYwZC1iMGY0LWZjOTI1YTJiNDcxYyIsImMiOjh9&pageName=ReportSection6210f47c91b423ca77de"
driver.get(url)

# Wait for the dashboard to fully load
wait = WebDriverWait(driver, 30)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='row']")))

# Function to extract table data
def extract_data():
    rows = driver.find_elements(By.CSS_SELECTOR, "div[role='row']")
    data = []

    for row in rows:
        cells = row.find_elements(By.CSS_SELECTOR, "div[role='gridcell']")
        row_data = [cell.text.strip() for cell in cells]
        if row_data:  # Avoid empty rows
            data.append(row_data)

    return data

# Extract all data
all_data = extract_data()

# Check if pagination exists
try:
    next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Next Page']")
    while next_button.is_enabled():
        next_button.click()
        time.sleep(5)  # Wait for the new page to load
        all_data.extend(extract_data())  # Append new page data
        next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Next Page']")
except:
    print("No pagination found or all pages scraped.")

# Convert to DataFrame
df = pd.DataFrame(all_data)

# Save data to CSV
df.to_csv("powerbi_full_data.csv", index=False)
print("Data successfully saved!")

driver.quit()
