from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Setup Selenium WebDriver
options = Options()
options.headless = False  # Change to True if you don't want the browser to open
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Open the Power BI dashboard
url = "https://www.oecd.org/en/data/tools/beps-mli-matching-database.html"
driver.get(url)

# Wait for Power BI container to load
wait = WebDriverWait(driver, 15)
powerbi_container = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.visualWrapper.report"))
)

# Extract data from Power BI container
visuals = powerbi_container.find_elements(By.TAG_NAME, "div")

data = []
for visual in visuals:
    try:
        text = visual.text.strip()
        if text:
            data.append(text)
    except:
        pass  # Ignore any errors

# Convert to DataFrame and Save
df = pd.DataFrame(data, columns=["Extracted Data"])
df.to_csv("powerbi_oecd_data.csv", index=False)

print("Data saved successfully!")

# Close browser
driver.quit()
