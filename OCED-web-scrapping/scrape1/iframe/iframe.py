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
options.headless = False  # Set to True for headless mode
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Open the OECD Power BI Dashboard page (which contains the iframe)
url = "https://www.oecd.org/en/data/tools/beps-mli-matching-database.html"
driver.get(url)

# Wait for the Power BI iframe to appear
wait = WebDriverWait(driver, 20)
iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))

# Switch to the Power BI iframe
driver.switch_to.frame(iframe)

# Wait for Power BI table data to load
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

# Extract all available data
all_data = extract_data()

# Handle pagination (if applicable)
try:
    next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Next Page']")
    while next_button.is_enabled():
        next_button.click()
        time.sleep(5)  # Wait for new page data to load
        all_data.extend(extract_data())  # Append data from new page
        next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Next Page']")
except:
    print("No pagination found or all pages scraped.")

# Convert to DataFrame
df = pd.DataFrame(all_data)

# Save data to CSV
df.to_csv("powerbi_oecd_data.csv", index=False)
print("Data successfully saved to 'powerbi_oecd_data.csv'")

# Close the browser
driver.quit()
