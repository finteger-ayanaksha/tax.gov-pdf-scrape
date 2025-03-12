import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup Selenium
options = Options()
options.headless = False  # Set to True for headless mode
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Open Power BI Dashboard
url = "https://app.powerbi.com/view?r=eyJrIjoiYmQ5NGE3M2EtNTdhZi00NTFkLTkxNzEtNzQzMWU0NjBmYTI5IiwidCI6ImFjNDFjN2Q0LTFmNjEtNDYwZC1iMGY0LWZjOTI1YTJiNDcxYyIsImMiOjh9&pageName=ReportSection6210f47c91b423ca77de"
driver.get(url)

# Wait for Power BI report to load
time.sleep(10)  # Increase if needed

# Extract Table Data
rows = driver.find_elements(By.CSS_SELECTOR, "div[role='row']")
data = []

for row in rows:
    cells = row.find_elements(By.CSS_SELECTOR, "div[role='gridcell']")
    data.append([cell.text.strip() for cell in cells])

# Convert to DataFrame
df = pd.DataFrame(data)
df.to_csv("powerbi_scraped_data.csv", index=False)

print("Data saved successfully!")

driver.quit()
