from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_data_for_date(date, date_picker, wait, all_data, data_xpaths):
    """
    Function to input a date, trigger the search, and extract data from multiple divs.
    """
    try:
        date_picker.clear()
        date_picker.send_keys(date)
        date_picker.send_keys(Keys.RETURN)
        time.sleep(5) 
        time.sleep(10) 

        extracted_values = [date]
        
        for div_xpath in data_xpaths:
            extracted_text = get_data_from_div(wait, div_xpath)
            extracted_values.append(extracted_text)
        
        all_data.append(extracted_values)

    except Exception as e:
        print(f"Error processing date {date}: {e}")

def get_data_from_div(wait, div_xpath):
    """
    Function to extract text from a specified div element using XPath.
    """
    try:
        data_container = wait.until(EC.presence_of_element_located((By.XPATH, div_xpath)))
        return data_container.text.strip()
    except Exception as e:
        print(f" Failed to extract data from {div_xpath}: {e}")
        return "N/A"

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

# List of XPaths for different divs
data_xpaths = [
    '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-group[2]/transform/div/div[2]/visual-container-group/transform/div/div[2]/visual-container[4]/transform/div/div[3]/div/div/visual-modern/div/div/div[2]/div[1]',
    '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-group[3]/transform/div/div[2]/visual-container-group/transform/div/div[2]/visual-container[5]/transform/div/div[3]/div/div/visual-modern/div/div/div[2]/div[1]',
    '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-group[4]/transform/div/div[2]/visual-container-group/transform/div/div[2]/visual-container[6]/transform/div/div[3]/div/div/visual-modern/div/div/div[2]/div[1]',
    '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-group[5]/transform/div/div[2]/visual-container-group/transform/div/div[2]/visual-container[7]/transform/div/div[3]/div/div/visual-modern/div/div/div[2]/div[1]',
]

# Scrape data for each date
for date in dates:
    scrape_data_for_date(date, date_picker, wait, all_data, data_xpaths)

# Convert to DataFrame
columns = ["Date"] + [f"Div_{i+1}" for i in range(len(data_xpaths))]
df = pd.DataFrame(all_data, columns=columns)

df.to_csv("PowerBI_Extracted_Data2.csv", index=False)
print(" Scraping Completed Successfully! Data saved to PowerBI_Extracted_Data.csv")

driver.quit()
