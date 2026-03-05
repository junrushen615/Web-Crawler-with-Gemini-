import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
import requests_cache
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin
from tqdm import tqdm
import os

BASE_URL = "https://openaccess.thecvf.com/CVPR2025"
SEARCH_KEYWORD = "deep learning"
OUTPUT_FILE = "cvpr_2025_deep_learning_papers.csv"
USER_AGENT = "CVPR_Crawler_Bot/1.0 (+https://yourdomain.com)"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("crawler.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

session = requests_cache.CachedSession('cvpr_cache', expire_after=604800)

retry_strategy = Retry(
    total=5,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)

def check_robots_txt(url, user_agent):
    robots_url = urljoin(url, "/robots.txt")
    rp = RobotFileParser()
    try:
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception as e:
        logging.warning(f"Could not read robots.txt ({e}). Proceeding.")
        return True

def extract_paper_metadata(paper_url):
    try:
        response = session.get(paper_url, headers={"User-Agent": USER_AGENT}, timeout=15)
        
        if not getattr(response, 'from_cache', False):
            time.sleep(random.uniform(1.0, 3.0)) 
            
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        abstract_div = soup.find('div', id='abstract')
        abstract = abstract_div.text.strip() if abstract_div else ""
        
        authors_div = soup.find('div', id='authors')
        authors = authors_div.text.strip().replace('\n', '').replace(';', ', ') if authors_div else "Unknown"
        
        month_div = soup.find('div', class_='month')
        pub_date = f"{month_div.text.strip()} 2025" if month_div else "June 2025"
            
        return authors, abstract, pub_date
        
    except Exception as e:
        logging.error(f"Error accessing {paper_url}: {e}")
        return None, None, None

def run_crawler():
    if not check_robots_txt(BASE_URL, USER_AGENT):
        logging.error("Scraping is disallowed by robots.txt. Exiting.")
        return

    logging.info("Phase 1: Collecting all paper URLs...")
    current_url = f"{BASE_URL}?day=all"
    
    paper_links = set() 
    
    while current_url:
        try:
            response = session.get(current_url, headers={"User-Agent": USER_AGENT}, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            logging.error(f"Failed to fetch index page {current_url}: {e}")
            break

        paper_entries = soup.find_all('dt', class_='ptitle')
        if not paper_entries:
            break

        for entry in paper_entries:
            link_tag = entry.find('a')
            if link_tag:
                title = link_tag.text.strip()
                url = urljoin(BASE_URL, link_tag['href'])
                paper_links.add((title, url)) 

        next_button = soup.find('a', string=lambda text: text and 'Next' in text)
        if next_button and 'href' in next_button.attrs:
            current_url = urljoin(BASE_URL, next_button['href'])
        else:
            current_url = None

    logging.info(f"Collected {len(paper_links)} unique papers to process.")

    papers_data = []
    
    for title, paper_url in tqdm(paper_links, desc="Processing Papers", unit="paper"):
        authors, abstract, pub_date = extract_paper_metadata(paper_url)
        
        if not abstract:
            continue
            
        if (SEARCH_KEYWORD.lower() in title.lower()) or (SEARCH_KEYWORD.lower() in abstract.lower()):
            papers_data.append({
                "Title": title,
                "Authors": authors,
                "Abstract": abstract,
                "Publication Date": pub_date,
                "URL": paper_url
            })

    if papers_data:
        df = pd.DataFrame(papers_data)
        df.drop_duplicates(subset=['URL'], inplace=True) 
        df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
        logging.info(f"Success! Saved {len(df)} matching papers to '{OUTPUT_FILE}'.")
    else:
        logging.info("Finished crawling, but no papers matched your criteria.")

if __name__ == "__main__":
    run_crawler()