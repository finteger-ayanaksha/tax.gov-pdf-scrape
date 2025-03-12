from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

#  Setup Chrome WebDriver
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Uncomment for headless execution
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#  Open the OECD Page (Where Power BI is embedded)
oecd_url = "https://www.oecd.org/en/data/tools/beps-mli-matching-database.html"
driver.get(oecd_url)
wait = WebDriverWait(driver, 30)

#  Locate and Switch to the Power BI iframe
try:
    iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    driver.switch_to.frame(iframe)
    print(" Switched to Power BI iframe.")
except:
    print(" No iframe found! Ensure the Power BI dashboard is embedded here.")
    driver.quit()
    exit()

#  Now Interact with Elements Inside the iFrame
# date_picker_xpath = "//*[@id='30db48be-c1c9-9dd7-ce18-7924e28c0b46']"
possible_xpaths = [
    '//*[@id="30db48be-c1c9-9dd7-ce18-7924e28c0b46"]',  # ID-Based XPath (May Change)
    "//input[@class='date-slicer-datepicker']",  # Class-Based XPath
    "//input[@type='text' and contains(@aria-label, 'End date')]",  # Aria-Label XPath
    "//input[@type='text']",  # General Fallback (May Not Be Specific Enough)
]

date_picker = None
for xpath in possible_xpaths:
    try:
        date_picker = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        print(f" Date Picker Found Using XPath: {xpath}")
        break
    except:
        continue

if not date_picker:
    print("❌ Date Picker not found, check XPath manually.")
    driver.quit()
    exit()

#  Click Date Picker (Using JavaScript if Necessary)
driver.execute_script("arguments[0].click();", date_picker)

#  List of Dates to Scrape

# dates = ["3/1/2025", "2/1/2025"]
dates = ["3/1/2025"]
all_data = []

#  Loop Through Dates and Scrape Data
for date in dates:
    try:
        # Clear and Enter New Date
        date_picker.clear()
        date_picker.send_keys(date)
        date_picker.send_keys(Keys.RETURN)
        time.sleep(5)  # Wait for data refresh

        # Extract Table Data
        table_rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
        for row in table_rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            data = [col.text.strip() for col in cols]
            all_data.append([date] + data)

    except Exception as e:
        print(f" Error scraping for date {date}: {e}")

#  Save Data to CSV
df = pd.DataFrame(all_data, columns=["Date", "Category", "As of Selected Date", "Total as of Today"])
df.to_csv("OECD_PowerBI_Scraped_Data.csv", index=False)

driver.quit()
print(" Scraping Completed Successfully! Data saved to OECD_PowerBI_Scraped_Data.csv")
