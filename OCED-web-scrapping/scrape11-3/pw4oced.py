# from playwright.sync_api import sync_playwright
# import time

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)  # Set headless=True if you don't need UI
#     page = browser.new_page()
    
#     # Go to the page
#     page.goto("https://www.oecd.org/en/data/tools/beps-mli-matching-database.html", timeout=60000)
    
#     # Optional: Wait for page to load completely
#     time.sleep(5)  # Give a few seconds for page load

#     # Wait for the first <p> element in div.cmp-text to be attached or visible
#     try:
#         page.wait_for_selector("div.pivotTableCellWrap", state="attached", timeout=60000)

#         # Extract the text from the first <p> element inside div.cmp-text
#         title = page.inner_text("div.pivotTableCellWrap.cell-interactive.tablixAlignCenter.main-cell")

#         print("Extracted Title:", title)
#     except Exception as e:
#         print(f"An error occurred: {e}")

#     browser.close()




# work only for single one
# from playwright.sync_api import sync_playwright
# import time

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)  # Set headless=True if you don't need UI
#     page = browser.new_page()
    
#     # Go to the page
#     page.goto("https://www.oecd.org/en/data/tools/beps-mli-matching-database.html", timeout=20000)
    
#     # Optional: Wait for page to load completely
#     time.sleep(5)  # Give a few seconds for page load

#     # Wait for the first <p> element in div.cmp-text to be attached or visible
#     try:
#         page.wait_for_selector("h2.cmp-title__text", state="attached", timeout=20000)

#         # Extract the text from the first <p> element inside div.cmp-text
#         title = page.inner_text("h2.cmp-title__text")

#         print("Extracted Title:", title)
#     except Exception as e:
#         print(f"An error occurred: {e}")

#     browser.close()






from selectolax.parser import HTMLParser
from playwright.sync_api import sync_playwright

def extractBody(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        TIMEOUT = 30000
        
        page.wait_for_load_state("networkidle", timeout=TIMEOUT)
        
        locator = page.locator("h2.cmp-title__text")
        locator.wait_for(state="visible", timeout=TIMEOUT)

        return page.inner_html("body")

def extractBudget(html):
    tree = HTMLParser(html)
    budgetDivs = tree.css("h2.cmp-title__text")
    budgetData = []
    for div in budgetDivs:
        budgetData.append(div.text()) 
    return budgetData

if __name__ == "__main__":
    url = "https://www.oecd.org/en/data/tools/beps-mli-matching-database.html"
    html = extractBody(url)
    budgetData = extractBudget(html)
    
    for data in budgetData:
        print(data)
