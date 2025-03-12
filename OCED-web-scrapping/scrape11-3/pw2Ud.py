# from playwright.sync_api import sync_playwright

# url = "https://www.oecd.org/en/data/tools/beps-mli-matching-database.html"

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=True)  # Set headless=False if you want to see the browser
#     page = browser.new_page()
#     page.goto(url, timeout=30000)  # Load page with a timeout
    

#     title = page.inner_text("h2.cmp-title__text")
    
#     print("H1 Title:", title)

#     browser.close()




# from playwright.sync_api import sync_playwright

# url = "https://www.udemy.com/?utm_source=adwords-brand&utm_medium=udemyads&utm_campaign=Brand-Udemy_la.EN_cc.India_dev.&campaigntype=Search&portfolio=BrandDirect&language=EN&product=Course&test=&audience=Keyword&topic=&priority=&utm_content=deal4584&utm_term=_._ag_133043842301_._ad_595460368494_._kw_udemy_._de_c_._dm__._pl__._ti_aud-2297301418005:kwd-296956216253_._li_9062010_._pd__._&matchtype=b&gad_source=1&gclid=CjwKCAiAn9a9BhBtEiwAbKg6fkLMXs3aNNiJdIG9TrqIfxtlgpmn1Zx_HXro-ft6kk_bnm22QID9SBoC8o4QAvD_BwE"

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=True)  # Set headless=False if you want to see the browser
#     page = browser.new_page()
#     page.goto(url, timeout=30000)  # Load page with a timeout
    

#     title = page.inner_text("h3.ud-heading-xl")
    
#     print("H3 Title:", title)

#     browser.close()





# from playwright.sync_api import sync_playwright

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)  # Set headless=True if you don't need UI
#     page = browser.new_page()
    
#     page.goto("https://www.udemy.com/?utm_source=adwords-brand&utm_medium=udemyads&utm_campaign=Brand-Udemy_la.EN_cc.India_dev.&campaigntype=Search&portfolio=BrandDirect&language=EN&product=Course&test=&audience=Keyword&topic=&priority=&utm_content=deal4584&utm_term=_._ag_133043842301_._ad_595460368494_._kw_udemy_._de_c_._dm__._pl__._ti_aud-2297301418005:kwd-296956216253_._li_9062010_._pd__._&matchtype=b&gad_source=1&gclid=CjwKCAiAn9a9BhBtEiwAbKg6fkLMXs3aNNiJdIG9TrqIfxtlgpmn1Zx_HXro-ft6kk_bnm22QID9SBoC8o4QAvD_BwE", timeout=60000)  # Replace with actual URL

#     # Wait for the element to be visible
#     page.wait_for_selector("h1.ud-heading-serif-xxl", state="visible", timeout=60000)

#     # Extract text
#     title = page.inner_text("h1.ud-heading-serif-xxl")

#     print("Extracted Title:", title)

#     browser.close()





from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Set headless=True if you don't need UI
    page = browser.new_page()
    
    page.goto("https://www.udemy.com/?utm_source=adwords-brand&utm_medium=udemyads&utm_campaign=Brand-Udemy_la.EN_cc.India_dev.&campaigntype=Search&portfolio=BrandDirect&language=EN&product=Course&test=&audience=Keyword&topic=&priority=&utm_content=deal4584&utm_term=_._ag_133043842301_._ad_595460368494_._kw_udemy_._de_c_._dm__._pl__._ti_aud-2297301418005:kwd-296956216253_._li_9062010_._pd__._&matchtype=b&gad_source=1&gclid=CjwKCAiAn9a9BhBtEiwAbKg6fkLMXs3aNNiJdIG9TrqIfxtlgpmn1Zx_HXro-ft6kk_bnm22QID9SBoC8o4QAvD_BwE", timeout=40000)  # Replace with actual URL

    # Wait for the element to be visible
    page.wait_for_selector("span.ud-heading-md", state="visible", timeout=40000)

    # Extract text
    title = page.inner_text("span.ud-heading-md")

    print("Extracted Title:", title)

    browser.close()

    
