from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Set up Selenium
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# Open the website
url = "https://www.oecd.org/en/data/tools/beps-mli-matching-database.html"
driver.get(url)

# Extract the target div
element = driver.find_element(By.CSS_SELECTOR, "div[_ngcontent-ng-c814307280]")  # Modify if necessary

print(element.text)  # Extract text inside the div

driver.quit()
