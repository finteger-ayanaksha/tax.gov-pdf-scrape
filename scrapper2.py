import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import logging
import re
from urllib.parse import urljoin
import argparse
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("tax_scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TaxDocumentScraper:
    def __init__(self, target_date=None):
        self.base_url = "https://tax.gov.ae/en/legislation.aspx"
        
        # Set target date (either provided or today)
        if target_date:
            self.target_date = target_date
            self.target_date_obj = datetime.strptime(target_date, "%b %d, %Y")
            folder_date = self.target_date_obj.strftime("%Y-%m-%d")
        else:
            self.target_date = datetime.now().strftime("%b %d, %Y")
            folder_date = datetime.now().strftime("%Y-%m-%d")
            
        self.download_folder = self._create_download_folder(folder_date)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        logger.info(f"Targeting documents published on: {self.target_date}")
    
    def _create_download_folder(self, folder_date):
        """Create a folder for the targeted date's downloads"""
        target_folder = os.path.join(
            "tax_documents", 
            folder_date
        )
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
            logger.info(f"Created download folder: {target_folder}")
        return target_folder
    
    def _clean_filename(self, filename):
        """Clean filename to remove invalid characters"""
        return re.sub(r'[\\/*?:"<>|]', "", filename)
    
    def get_page_content(self):
        """Fetch the legislation page content"""
        try:
            logger.info(f"Fetching content from {self.base_url}")
            response = requests.get(self.base_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching page content: {e}")
            return None
    
    def parse_documents(self, html_content):
        """Parse the HTML to find documents published on the target date"""
        if not html_content:
            return []
        
        soup = BeautifulSoup(html_content, 'html.parser')
        target_documents = []
        
        # Find all document rows based on the provided HTML structure
        document_rows = soup.find_all('div', class_='row')
        
        for row in document_rows:
            try:
                # Skip header rows or rows without proper structure
                if 'headerTable' in row.get('class', []):
                    continue
                
                # Check if this is a document row (has title and date)
                title_div = row.find('div', class_='col-md-7')
                if not title_div:
                    continue
                
                # Extract title
                title_element = title_div.find('div', class_='d-flex')
                if not title_element:
                    continue
                
                title = title_element.get_text(strip=True).split('New')[0].strip()
                
                # Extract publish date
                date_rows = title_div.find_all('div', class_='row no-gutters')
                if not date_rows:
                    continue
                
                for date_row in date_rows:
                    date_spans = date_row.find_all('span', class_='lastmodifiedDate')
                    date_captions = date_row.find_all('span', class_='lastmodifiedDateCaption')
                    
                    # Match publish date and its caption
                    for i, caption in enumerate(date_captions):
                        if 'Publish Date' in caption.text and i < len(date_spans):
                            publish_date = date_spans[i].text.strip()
                            
                            # Check if this document was published on the target date
                            if publish_date == self.target_date:
                                # Get the download link
                                download_div = row.find('div', class_='downloadlinks')
                                if download_div and download_div.find('a'):
                                    download_link = download_div.find('a')['href']
                                    if download_link:
                                        # Make sure we have the full URL
                                        if not download_link.startswith('http'):
                                            download_link = urljoin('https://tax.gov.ae', download_link)
                                        
                                        # Extract category if available
                                        category = ""
                                        category_span = title_div.find('span', class_='tag_category')
                                        if category_span:
                                            category = category_span.text.strip()
                                        
                                        document_info = {
                                            'title': title,
                                            'url': download_link,
                                            'publish_date': publish_date,
                                            'category': category
                                        }
                                        
                                        target_documents.append(document_info)
                                        logger.info(f"Found document published on {self.target_date}: {title}")
            except Exception as e:
                logger.error(f"Error parsing document row: {e}")
                continue
        
        return target_documents
    
    def download_documents(self, documents):
        """Download all documents in the list"""
        if not documents:
            logger.info(f"No documents found for the date: {self.target_date}")
            return
        
        logger.info(f"Attempting to download {len(documents)} documents")
        
        for doc in documents:
            try:
                response = requests.get(doc['url'], headers=self.headers, timeout=60)
                response.raise_for_status()
                
                # Try to get filename from content-disposition header
                filename = None
                content_disposition = response.headers.get('Content-Disposition')
                if content_disposition:
                    filename_match = re.search(r'filename="?([^"]+)"?', content_disposition)
                    if filename_match:
                        filename = filename_match.group(1)
                
                # If filename not found in header, extract from URL
                if not filename:
                    filename = os.path.basename(doc['url'])
                
                # Clean filename if needed
                filename = self._clean_filename(filename)
                
                # If filename still empty or invalid, use the title
                if not filename or filename == "":
                    # Determine file extension from URL or content-type
                    file_extension = os.path.splitext(doc['url'])[1]
                    if not file_extension:
                        content_type = response.headers.get('Content-Type', '')
                        if 'pdf' in content_type.lower():
                            file_extension = '.pdf'
                        elif 'word' in content_type.lower():
                            file_extension = '.docx'
                        else:
                            file_extension = '.pdf'  # Default to PDF
                    
                    # Create filename from title
                    filename = self._clean_filename(doc['title']) + file_extension
                
                # Create category subfolder if available
                if doc.get('category') and doc['category'].strip():
                    category_folder = os.path.join(self.download_folder, self._clean_filename(doc['category']))
                    if not os.path.exists(category_folder):
                        os.makedirs(category_folder)
                    file_path = os.path.join(category_folder, filename)
                else:
                    file_path = os.path.join(self.download_folder, filename)
                
                # Save file
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                
                logger.info(f"Downloaded: {filename}")
            except Exception as e:
                logger.error(f"Error downloading {doc['title']}: {e}")
    
    def run(self):
        """Execute the full scraping process"""
        logger.info(f"Starting UAE Tax Authority document scraper for date: {self.target_date}")
        html_content = self.get_page_content()
        documents = self.parse_documents(html_content)
        self.download_documents(documents)
        logger.info(f"Scraping completed. Downloaded {len(documents)} documents published on {self.target_date}.")


def parse_date(date_str):
    """Convert various date formats to the format used on the website"""
    try:
        # Try different date formats
        for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y', '%b %d, %Y', '%B %d, %Y'):
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime('%b %d, %Y')  # Format as "Feb 26, 2025"
            except ValueError:
                continue
        
        # If none of the formats match
        raise ValueError(f"Date format not recognized: {date_str}")
    except Exception as e:
        logger.error(f"Error parsing date: {e}")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download tax documents published on a specific date')
    parser.add_argument('-d', '--date', type=str, help='Target date (e.g., "Mar 03, 2025", "2025-03-03", "03/03/2025")')
    
    args = parser.parse_args()
    
    try:
        if args.date:
            target_date = parse_date(args.date)
            scraper = TaxDocumentScraper(target_date=target_date)
        else:
            # If no date provided, use today
            scraper = TaxDocumentScraper()
            
        scraper.run()
    except Exception as e:
        logger.error(f"Script execution failed: {e}")
        sys.exit(1)