1. Internet `retry`

Gemini:
response = requests.get(paper_url, headers={"User-Agent": USER_AGENT}, timeout=10)

Upgraded_Gemini:
session = requests_cache.CachedSession('cvpr_cache', expire_after=604800)

retry_strategy = Retry(
    total=5,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)

2. Caching avoids duplicate requests. Establish a `session` with local caching. (Expired in 7 days)

session = requests_cache.CachedSession('cvpr_cache', expire_after=604800)
if not getattr(response, 'from_cache', False):
    time.sleep(random.uniform(1.0, 3.0))

3. Display progress by using `tqdm` to wrap the loop and display a progress bar in the console.

from tqdm import tqdm
for title, paper_url in tqdm(paper_links, desc="Processing Papers", unit="paper"):

4. Random latency, no latency when reading from the cache

if not getattr(response, 'from_cache', False):
    time.sleep(random.uniform(1.0, 3.0))

5. Enable background operation: Configure logging to prevent print information from being lost when running in the background.

Gemini:
print(f"--- Crawling Page {page_num}: {current_url} ---")

Updated_Gemini:
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("crawler.log", encoding='utf-8'),  # 写入文件
        logging.StreamHandler()  # 同时输出到控制台
    ]
)

6. Deduplication

(1)paper_links = set()
(2)df.drop_duplicates(subset=['URL'], inplace=True)





