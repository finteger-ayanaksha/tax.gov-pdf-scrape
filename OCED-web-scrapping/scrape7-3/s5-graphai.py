from scrapegraph_py import Client
from scrapegraph_py.logger import sgai_logger

sgai_logger.set_logging(level="INFO")

# Initialize the client
sgai_client = Client(api_key="sgai-f003ec69-646a-43e4-90cb-ac1f14617d64")
# SmartScraper request
response = sgai_client.smartscraper(
    website_url="https://app.powerbi.com/view?r=eyJrIjoiYmQ5NGE3M2EtNTdhZi00NTFkLTkxNzEtNzQzMWU0NjBmYTI5IiwidCI6ImFjNDFjN2Q0LTFmNjEtNDYwZC1iMGY0LWZjOTI1YTJiNDcxYyIsImMiOjh9&pageName=ReportSection6210f47c91b423ca77de",
    user_prompt="extract me the powerbi dashboard data to csv"
)

# Print the response
print(f"Request ID: {response['request_id']}")
print(f"Result: {response['result']}")

sgai_client.close()