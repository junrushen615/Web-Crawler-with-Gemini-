# Web_Crawler

## Description
This project is a Python-based web crawler designed to automate the extraction of research paper data from academic conference repositories, such as the Computer Vision Foundation (CVF) Open Access website. 

By default, the script targets CVPR 2025 and filters for papers related to "deep learning." It extracts the **Title**, **Authors**, **Abstract**, **Publication Date**, and **URL** of matching papers, saving the output neatly into a CSV file. 

The crawler is highly customizable; you can easily modify the target URL and search keywords to scrape papers from other conferences (e.g., ICCV, WACV, NeurIPS) or search for different topics, depending on your research needs.

## Environment Requirements

This project requires **Python 3.7 or higher**. 

To run the script, you will need to install the following Python packages:

* `requests`
* `beautifulsoup4`
* `pandas`
* `requests-cache`
* `tqdm`
* `urllib3`

You can install all required dependencies at once using `pip`:

```bash
pip install requests beautifulsoup4 pandas requests-cache tqdm urllib3
```
## Usage steps
1. To run the crawler with its default settings (searching for "deep learning" papers in CVPR 2025), simply execute the updated python script from your terminal.
2. Customizing the target Conference and keyword based on your demands.

## Acknowledgements
I would like to acknowledge Gemini for the initial coding, as well as ChatGPT and GitHub Copilot for their valuable coding suggestions.
