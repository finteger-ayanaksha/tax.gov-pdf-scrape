# Install with pip install firecrawl-py
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key='fc-819c766b27cb4ab5833c47748b413cb8')

response = app.scrape_url(url='https://www.oecd.org/en/data/tools/beps-mli-matching-database.html', params={
	'formats': [ 'markdown', 'html' ],
})