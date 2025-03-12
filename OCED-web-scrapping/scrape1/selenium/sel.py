import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Setup Selenium WebDriver
options = Options()
options.headless = False  
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Open the Power BI dashboard
url = "https://app.powerbi.com/view?r=eyJrIjoiYmQ5NGE3M2EtNTdhZi00NTFkLTkxNzEtNzQzMWU0NjBmYTI5IiwidCI6ImFjNDFjN2Q0LTFmNjEtNDYwZC1iMGY0LWZjOTI1YTJiNDcxYyIsImMiOjh9&pageName=ReportSection6210f47c91b423ca77de"
driver.get(url)

# Wait for the Power BI iframe to load
time.sleep(10)  

# Screenshot the report (for OCR extraction if necessary)
driver.save_screenshot("powerbi_screenshot.png")

print("Screenshot saved: powerbi_screenshot.png")

driver.quit()
