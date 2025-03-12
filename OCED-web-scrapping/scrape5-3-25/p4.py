from playwright.sync_api import sync_playwright
import pandas as pd

def scrape_power_bi_playwright(url):
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Navigate to URL
            page.goto(url, wait_until='networkidle')
            
            # Extract table data using JavaScript
            table_data = page.evaluate('''() => {
                const tables = document.querySelectorAll('table');
                return Array.from(tables).map(table => {
                    return Array.from(table.querySelectorAll('tr')).map(row => 
                        Array.from(row.querySelectorAll('td, th')).map(cell => cell.textContent.trim())
                    );
                });
            }''')
            
            # Convert to DataFrame
            df = pd.DataFrame(table_data[0][1:], columns=table_data[0][0])
            return df
        
        except Exception as e:
            print(f"Scraping error: {e}")
            return None
        
        finally:
            browser.close()

# Example usage
url = 'https://www.oecd.org/en/data/tools/beps-mli-matching-database.html'
scraped_data = scrape_power_bi_playwright(url)

if scraped_data is not None:
    print(scraped_data)