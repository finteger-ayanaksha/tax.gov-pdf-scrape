# from playwright.sync_api import sync_playwright

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=True)  # Set headless=False for debugging
#     page = browser.new_page()
    
#     page.goto("https://www.oecd.org/en.html", timeout=30000)  # Replace with the actual URL

#     # Wait for the div to load
#     page.wait_for_selector("div.cmp-text", timeout=30000)

#     # Extract text from the <p> inside the div with class "cmp-text"
#     text_content = page.inner_text("div.cmp-text")

#     print("Extracted Text:", text_content)

#     browser.close()



# heading-done
# from playwright.sync_api import sync_playwright

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)  # Set headless=True if you don't need UI
#     page = browser.new_page()
    
#     page.goto("https://www.oecd.org/en/about/news/press-releases/2025/03/czechia-must-ensure-fiscal-sustainability-and-boost-skills-innovation-and-business-dynamism-to-drive-growth-says-oecd.html", timeout=30000)  # Replace with actual URL

#     # Wait for the element to be visible
#     page.wait_for_selector("h1.cmp-article-header__title", state="visible", timeout=30000)

#     # Extract text
#     title = page.inner_text("h1.cmp-article-header__title")

#     print("Extracted Title:", title)

#     browser.close()





# from playwright.sync_api import sync_playwright

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)  # Set headless=True if you don't need UI
#     page = browser.new_page()
    
#     page.goto("https://www.oecd.org/en/about/news/press-releases/2025/03/czechia-must-ensure-fiscal-sustainability-and-boost-skills-innovation-and-business-dynamism-to-drive-growth-says-oecd.html", timeout=30000)  # Replace with actual URL

#     # Wait for the element to be visible
#     page.wait_for_selector("div.cmp-text p", state="visible", timeout=30000)

#     # Extract text
#     title = page.inner_text("div.cmp-text p")

#     print("Extracted Title:", title)

#     browser.close()


# idk p tag from where its coming
# from playwright.sync_api import sync_playwright
# import time

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)  # Set headless=True if you don't need UI
#     page = browser.new_page()
    
#     # Go to the page
#     page.goto("https://www.oecd.org/en/about/news/press-releases/2025/03/czechia-must-ensure-fiscal-sustainability-and-boost-skills-innovation-and-business-dynamism-to-drive-growth-says-oecd.html", timeout=30000)
    
#     # Optional: Wait for page to load completely
#     time.sleep(5)  # Give a few seconds for page load

#     # Wait for the first <p> element in div.cmp-text to be attached or visible
#     try:
#         page.wait_for_selector("div.cmp-text p", state="attached", timeout=30000)

#         # Extract the text from the first <p> element inside div.cmp-text
#         title = page.inner_text("div.cmp-text p:first-child")

#         print("Extracted Title:", title)
#     except Exception as e:
#         print(f"An error occurred: {e}")

#     browser.close()


from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Set headless=True if you don't need UI
    page = browser.new_page()
    
    # Go to the page
    page.goto("https://app.powerbi.com/view?r=eyJrIjoiYmQ5NGE3M2EtNTdhZi00NTFkLTkxNzEtNzQzMWU0NjBmYTI5IiwidCI6ImFjNDFjN2Q0LTFmNjEtNDYwZC1iMGY0LWZjOTI1YTJiNDcxYyIsImMiOjh9&pageName=ReportSection6210f47c91b423ca77de", timeout=30000)
    
    # Optional: Wait for page to load completely
    time.sleep(5)  # Give a few seconds for page load

    # Wait for the first <p> element in div.cmp-text to be attached or visible
    try:
        page.wait_for_selector("div.pivotTableCellNoWrap", state="attached", timeout=30000)

        # Extract the text from the first <p> element inside div.cmp-text
        title = page.inner_text("div.pivotTableCellNoWrap")

        print("Extracted Title:", title)
    except Exception as e:
        print(f"An error occurred: {e}")

    browser.close()