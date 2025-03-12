from selectolax.parser import HTMLParser
from playwright.sync_api import sync_playwright

def extractBody(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        TIMEOUT = 35000
        
        # Wait for the page to fully load
        page.wait_for_load_state("networkidle", timeout=TIMEOUT)
        
        # Using locator instead of wait_for_selector
        locator = page.locator("div.cmp-generic-header__content-area")
        locator.wait_for(state="visible", timeout=TIMEOUT)

        # Get the inner HTML of the body
        return page.inner_html("body")

def extractBudget(html):
    tree = HTMLParser(html)
    budgetDivs = tree.css("div.cmp-generic-header__content-area")
    budgetData = []
    for div in budgetDivs:
        budgetData.append(div.text()) 
    return budgetData

if __name__ == "__main__":
    url = "https://www.oecd.org/en/data/tools/beps-mli-matching-database.html"
    html = extractBody(url)
    budgetData = extractBudget(html)
    
    # Print the extracted budget data
    for data in budgetData:
        print(data)
