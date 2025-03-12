from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Setup Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run without opening browser (optional)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open Power BI Dashboard
dashboard_url = "https://app.powerbi.com/view?r=eyJrIjoiYmQ5NGE3M2EtNTdhZi00NTFkLTkxNzEtNzQzMWU0NjBmYTI5IiwidCI6ImFjNDFjN2Q0LTFmNjEtNDYwZC1iMGY0LWZjOTI1YTJiNDcxYyIsImMiOjh9&pageName=ReportSectionba11fdb2c065e68183e7"
driver.get(dashboard_url)
wait = WebDriverWait(driver, 20)

# Wait for Full Page Load
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

# Handle iFrame (Uncomment if applicable)
# iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
# driver.switch_to.frame(iframe)

# Updated XPath (Try alternative if ID is dynamic)
date_picker_xpath = "//*[@id='30db48be-c1c9-9dd7-ce18-7924e28c0b46']"
# Alternative XPath: "//input[@type='text' and contains(@aria-label, 'Status as of')]"

# Ensure Date Picker is Clickable
date_picker = wait.until(EC.presence_of_element_located((By.XPATH, date_picker_xpath)))
date_picker = wait.until(EC.element_to_be_clickable((By.XPATH, date_picker_xpath)))

# JavaScript Click (For Hidden Elements)
driver.execute_script("arguments[0].click();", date_picker)

# Loop Through Dates
dates = ["2/10/2022", "2/11/2022", "2/12/2022"]
all_data = []

for date in dates:
    try:
        # Enter Date
        date_picker.clear()
        date_picker.send_keys(date)
        date_picker.send_keys(Keys.RETURN)
        time.sleep(3)  # Wait for page update

        # Extract Table Data
        table_rows = driver.find_elements(By.XPATH, "//table/tbody/tr")

        for row in table_rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            data = [col.text.strip() for col in cols]
            all_data.append([date] + data)

    except Exception as e:
        print(f"Error scraping for date {date}: {e}")

# Save Data
df = pd.DataFrame(all_data, columns=["Date", "Category", "As of Selected Date", "Total as of Today"])
df.to_csv("PowerBI_Scraped_Data.csv", index=False)

driver.quit()
print("✅ Scraping completed successfully!")
