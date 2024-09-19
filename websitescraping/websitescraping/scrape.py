import requests
from bs4 import BeautifulSoup
from home.log_config import configure_logger
from urllib.parse import urljoin, urlparse
import threading
from functools import lru_cache

logger = configure_logger(__name__)


@lru_cache(maxsize=128)
def is_valid_website(url):
    try:
        response = requests.head(url, timeout=2)  # Use HEAD request and reduce timeout
        if response.status_code == 200:
            return True, None
        else:
            return False, f"Invalid status code: {response.status_code}"
    except requests.exceptions.Timeout:
        logger.error(f"Timeout error checking website validity: {url}")
        return False, "Timeout error"
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error checking website validity: {url}")
        return False, "Connection error"
    except requests.exceptions.RequestException as e:
        logger.error(f"Error checking website validity: {e}")
        return False, str(e)


def scrape_website(url, result):
    is_valid, error_message = is_valid_website(url)
    if not is_valid:
        logger.error(f"Website is not valid: {url}. Error: {error_message}")
        result.append(f"Error: {url} is not a valid website")
        return

    try:
        logger.info(f"Website is valid: {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            full_url = urljoin(url, link['href'])
            if urlparse(url).netloc == urlparse(full_url).netloc:  # Check if the URL belongs to the same domain
                result.append(full_url)
    except Exception as e:
        logger.error(f"Error scraping website: {e}")
        result.append(f"Error: {e}")


def thread_scrape(urls):
    threads = []
    results = [[] for _ in urls]  # Create a list to hold results for each URL

    for i, url in enumerate(urls):
        thread = threading.Thread(target=scrape_website, args=(url, results[i]))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Flatten the list of results
    all_results = [url for sublist in results for url in sublist]
    return all_results