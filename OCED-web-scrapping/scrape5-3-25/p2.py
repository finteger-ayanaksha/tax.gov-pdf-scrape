from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
# Set up Selenium options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")



# Set up Selenium
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# chrome_driver_path = "/usr/local/bin/chromedriver"  # Mac/Linux

service = Service(driver)

# Open the target website
url = "https://www.oecd.org/en/data/tools/beps-mli-matching-database.html"
driver.get(url)

# Wait for page to load completely
time.sleep(5)

# Locate the target div by class name (modify if needed)
target_div = driver.find_element(By.CSS_SELECTOR, "div[_ngcontent-ng-c814307280]")

# Find all rows inside the div
rows = target_div.find_elements(By.CSS_SELECTOR, "div[role='row']")

# Extract data
data = []
for row in rows:
    columns = row.find_elements(By.CSS_SELECTOR, "div")  # Modify if needed
    row_data = [col.text for col in columns]
    if row_data:
        data.append(row_data)

# Save data to CSV
df = pd.DataFrame(data)
df.to_csv("scraped_data.csv", index=False)

print("Data successfully scraped and saved to scraped_data.csv")

# Close browser
driver.quit()
