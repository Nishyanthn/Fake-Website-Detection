import string
from urllib.parse import urlparse
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def is_url_live(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def generate_suspicious_urls(original_url):
    parsed = urlparse(original_url)
    domain_parts = parsed.netloc.split('.')
    suspicious_urls = []

    # Typosquatting: Slight misspellings (e.g., goolge.com instead of google.com)
    for part in domain_parts:
        if len(part) > 2:
            # Generate slight misspellings by replacing one or two characters
            for i in range(len(part)):
                for char in string.ascii_lowercase:
                    typo_url = original_url.replace(part[i], char, 1)
                    suspicious_urls.append(typo_url)

    # Homoglyphs: Characters that look similar (e.g., "o" with "0")
    homoglyph_map = {'o': '0', 'I': '1', 'a': '@', 'e': '3', 's': '5'}

    for part in domain_parts:
        for char, replacement in homoglyph_map.items():
            # Only replace in the domain part
            if char in part:
                homoglyph_url = original_url.replace(part, part.replace(char, replacement))
                suspicious_urls.append(homoglyph_url)

    # TLD variations: Add different TLDs (e.g., google.org instead of google.com)
    tlds = ['.com', '.org', '.net', '.ac', '.in', '.co']
    for tld in tlds:
        suspicious_urls.append(original_url.replace(domain_parts[-1], tld.strip('.')))

    # Prefix/Suffix variations
    prefix_suffix = ['www.', 'secure.', 'admin.']
    for prefix in prefix_suffix:
        suspicious_urls.append(parsed.scheme + "://" + prefix + parsed.netloc)

    # Generate http/https variations
    http_https_urls = []
    for url in suspicious_urls:
        http_https_urls.append(url.replace("https://", "http://"))
        http_https_urls.append(url.replace("http://", "https://"))

    # Use multithreading to check liveness of URLs
    live_urls = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Map is_url_live function over the URLs
        future_to_url = {executor.submit(is_url_live, url): url for url in http_https_urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                if future.result():  # If the URL is live, add it to the live URLs
                    live_urls.append(url)
                    print(f"Live URL found: {url}")  # Immediate feedback
            except Exception as e:
                print(f"Error checking URL {url}: {e}")
    
    return live_urls