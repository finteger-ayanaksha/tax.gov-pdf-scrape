from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

oecd_url = "https://www.oecd.org/en/data/tools/beps-mli-matching-database.html"
driver.get(oecd_url)
wait = WebDriverWait(driver, 30)

try:
    iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    driver.switch_to.frame(iframe)
    print(" Switched to Power BI iframe.")
except:
    print(" No iframe found! Ensure the Power BI dashboard is embedded here.")
    driver.quit()
    exit()

possible_xpaths = [
    '//*[@id="30db48be-c1c9-9dd7-ce18-7924e28c0b46"]',
    "//input[@class='date-slicer-datepicker']",
    "//input[@type='text' and contains(@aria-label, 'End date')]",
    "//input[@type='text']",
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
    print(" Date Picker not found, check XPath manually.")
    driver.quit()
    exit()

driver.execute_script("arguments[0].click();", date_picker)

dates = ["3/3/2025"]
all_data = []

for date in dates:
    try:
        date_picker.clear()
        date_picker.send_keys(date)
        date_picker.send_keys(Keys.RETURN)
        time.sleep(5)

        time.sleep(10)

        data_div_xpath = '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-group[2]/transform/div/div[2]/visual-container-group/transform/div/div[2]/visual-container[4]/transform/div/div[3]/div/div/visual-modern/div/div/div[2]/div[1]'

        try:
            data_container = wait.until(EC.presence_of_element_located((By.XPATH, data_div_xpath)))
            extracted_text = data_container.text.strip()
            print(f" Extracted Data: {extracted_text}")

            all_data.append([date, extracted_text])

        except Exception as e:
            print(f" Failed to extract data for {date}: {e}")

    except Exception as e:
        print(f"Error processing date {date}: {e}")

df = pd.DataFrame(all_data, columns=["Date", "Extracted Data"])
df.to_csv("PowerBI_Extracted_Data.csv", index=False)

print(" Scraping Completed Successfully! Data saved to PowerBI_Extracted_Data1.csv")

driver.quit()