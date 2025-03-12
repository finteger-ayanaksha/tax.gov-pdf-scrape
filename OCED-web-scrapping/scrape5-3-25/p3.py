import os
import json
import time
import logging
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("powerbi_scraper.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

class PowerBIScraper:
    def __init__(self):
        self.base_url = "https://www.oecd.org/en/data/tools/beps-mli-matching-database.html"
        self.download_folder = self._create_download_folder()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/"
        }
        self.driver = self._setup_selenium()

    def _create_download_folder(self):
        """Create a folder for today's downloads"""
        today_folder = os.path.join("powerbi_data", datetime.now().strftime("%Y-%m-%d"))
        if not os.path.exists(today_folder):
            os.makedirs(today_folder)
            logger.info(f"Created download folder: {today_folder}")
        return today_folder

    def _setup_selenium(self):
        """Setup Selenium with headless Chrome"""
        options = Options()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver

    def get_page_content(self):
        """Fetch the webpage content using Selenium"""
        try:
            logger.info(f"Fetching content from {self.base_url}")
            self.driver.get(self.base_url)
            time.sleep(5)  # Wait for the page to fully load
            return self.driver.page_source
        except Exception as e:
            logger.error(f"Error fetching page content: {e}")
            return None

    def extract_powerbi_data(self, html_content):
        """Extract Power BI iframe source and possible API data"""
        if not html_content:
            return None

        soup = BeautifulSoup(html_content, "html.parser")
        iframe = soup.find("iframe", {"src": True})

        if iframe:
            powerbi_url = iframe["src"]
            logger.info(f"Found Power BI Report URL: {powerbi_url}")
            return powerbi_url
        else:
            logger.warning("No Power BI iframe found on the page.")
            return None

    def extract_api_data(self, powerbi_url):
        """Extract potential API endpoints from the Power BI URL"""
        try:
            logger.info(f"Checking Power BI data source: {powerbi_url}")
            response = requests.get(powerbi_url, headers=self.headers, timeout=30)
            response.raise_for_status()

            # Check if JSON data is embedded in the response
            if "application/json" in response.headers.get("Content-Type", ""):
                data = response.json()
                logger.info("Extracted JSON data from Power BI.")
                return data
            else:
                logger.warning("No JSON data found in Power BI response.")
                return None

        except requests.RequestException as e:
            logger.error(f"Error fetching Power BI data: {e}")
            return None

    def save_data(self, data):
        """Save extracted data to a JSON file"""
        if not data:
            logger.info("No data to save.")
            return

        file_path = os.path.join(self.download_folder, "powerbi_data.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        logger.info(f"Power BI data saved: {file_path}")

    def run(self):
        """Execute the full scraping process"""
        logger.info("Starting Power BI Data Scraper")
        html_content = self.get_page_content()
        powerbi_url = self.extract_powerbi_data(html_content)

        if powerbi_url:
            data = self.extract_api_data(powerbi_url)
            self.save_data(data)

        logger.info("Scraping completed.")
        self.driver.quit()


if __name__ == "__main__":
    scraper = PowerBIScraper()
    scraper.run()
