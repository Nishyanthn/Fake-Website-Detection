from flask import Flask, render_template, request, jsonify
import requests
import difflib
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import whois  # Add this for domain checking
import ssl
import socket
import OpenSSL
from datetime import datetime
from flask_cors import CORS
# from database import insert_url, fetch_urls, update_url_status
# from url_generator import generate_suspicious_urls  
from url_generator import generate_suspicious_urls
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from urllib.parse import urlparse
import pickle


# Initialize Flask app
app = Flask(__name__)

# Enable CORS for React frontend
CORS(app)

# Load the Random Forest classifier model
with open('rf_classifier_model.pkl', 'rb') as file:
    rf_classifier = pickle.load(file)

def extract_features(url):
    # Create a dictionary to store the features
    features = {}
    
    # Parse the URL to extract hostname and other components
    parsed_url = urlparse(url)
    
    # Extracting some of the features based on your dataset
    # Extract only the selected features
    features['nb_www'] = url.count('www')
    features['ratio_digits_url'] = sum(c.isdigit() for c in url) / len(url) if len(url) > 0 else 0
    features['length_url'] = len(url)
    features['nb_slash'] = url.count('/')
    features['length_hostname'] = len(parsed_url.hostname) if parsed_url.hostname else 0
    features['nb_eq'] = url.count('=')
    features['ratio_digits_host'] = sum(c.isdigit() for c in parsed_url.hostname) / len(parsed_url.hostname) if parsed_url.hostname else 0
    features['tld_in_subdomain'] = 1 if parsed_url.hostname and parsed_url.hostname.endswith('.com') else 0
    features['nb_dots'] = url.count('.')
    features['nb_com'] = url.count('.com')
    features['nb_hyphens'] = url.count('-')
    features['nb_qm'] = url.count('?')

    # Return the extracted features
    return features


def log_function_start(function_name):
        print(f"{function_name} running... | Timestamp: {datetime.now()}") 

# Your existing functions for getting VirusTotal report, SSL validation, domain checking, etc.
def get_virustotal_report(url, api_key):
    log_function_start("get_virustotal_report")
    headers = {"x-apikey": api_key}
    url_encoded = requests.utils.quote(url)
    response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_encoded}", headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['data']['attributes']['last_analysis_stats']:
            positives = data['data']['attributes']['last_analysis_stats']['malicious']
            total = data['data']['attributes']['last_analysis_stats']['malicious'] + data['data']['attributes']['last_analysis_stats']['undetected']
            return positives, total
    return None, None

def validate_ssl_certificate(url):
    log_function_start("validate_ssl_certificate")
    try:
        hostname = url.split("://")[-1].split("/")[0]
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert(True)
                x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, cert)
                issuer = x509.get_issuer().CN
                expiration_date = datetime.strptime(x509.get_notAfter().decode('ascii'), "%Y%m%d%H%M%SZ")
                if expiration_date < datetime.now():
                    return f"The SSL certificate has expired. Issuer: {issuer}"
                if issuer == hostname:
                    return f"Self-signed certificate detected for {hostname}, which may be suspicious."
                return f"Valid SSL certificate issued by {issuer}, expires on {expiration_date.strftime('%Y-%m-%d')}."
    except Exception as e:
        return f"SSL certificate check failed: {str(e)}"

from bs4 import BeautifulSoup

def extract_text_from_html(html):
    """
    Extracts readable text from HTML, removes tags, scripts, and non-text content.
    
    :param html: Raw HTML content (as a string).
    :return: Extracted plain text from HTML.
    """
    soup = BeautifulSoup(html, 'lxml')
    # Remove scripts and style elements
    for script in soup(['script', 'style']):
        script.decompose()
    
    # Get the text and strip unnecessary whitespaces
    text = soup.get_text(" ", strip=True)
    
    return text

def scrape_url(url):
    log_function_start("scrape_url (original_html)")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(5)
        html = driver.page_source
        driver.quit()
        return html
    except WebDriverException as e:
        return None

def calculate_similarity(original_html, suspicious_html):
    log_function_start("calculate_similarity")
    
    # Extract text from HTML (assuming you already have a function for this)
    original_text = extract_text_from_html(original_html)
    suspicious_text = extract_text_from_html(suspicious_html)

    # Use TfidfVectorizer to convert text into TF-IDF vectors
    # tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([original_text, suspicious_text])

    
    # Calculate cosine similarity between the two text vectors
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    # Cosine similarity is a value between 0 and 1, where 1 means identical
    return cosine_sim[0][0] * 100  # Multiply by 100 to express it as a percentage


# def calculate_similarity(original, suspicious):
#     log_function_start("calculate_similarity")
#     return difflib.SequenceMatcher(None, original, suspicious).ratio() * 100

# def generate_suspicious_urls(original_url):
#     parsed = urlparse(original_url)
#     domain_parts = parsed.netloc.split('.')
#     suspicious_urls = []
#     for part in domain_parts:
#         if len(part) > 2:
#             suspicious_urls.append(parsed.scheme + "://" + part[:-1] + "0" + "." + ".".join(domain_parts[1:]))
#             suspicious_urls.append(parsed.scheme + "://" + part[:-1] + "@" + "." + ".".join(domain_parts[1:]))
#             suspicious_urls.append(parsed.scheme + "://" + part + "login." + ".".join(domain_parts[1:]))
#     return suspicious_urls

def check_domain_age(url):
    log_function_start("check_domain_age")
    try:
        domain = urlparse(url).netloc
        domain_info = whois.whois(domain)
        if isinstance(domain_info.creation_date, list):
            creation_date = domain_info.creation_date[0]
        else:
            creation_date = domain_info.creation_date
        if creation_date:
            age_days = (datetime.now() - creation_date).days
            if age_days < 90:
                return f"Domain registered recently ({age_days} days ago). Potentially suspicious."
            else:
                return f"Domain age is {age_days} days. Relatively established."
        else:
            return "Domain registration date is not available."
    except Exception as e:
        return f"Could not retrieve domain info: {str(e)}"
    


  #*first page**************** 
@app.route('/generate-urls', methods=['POST'])
def generate_urls():
    # Ensure you are parsing JSON correctly
    original_url = request.json.get('url')

    if not original_url:
        return jsonify({'error': 'No URL provided'}), 400

    # Generate suspicious URLs and check if they are live
    live_urls = generate_suspicious_urls(original_url)
    return jsonify({'live_urls': live_urls})   



 #*second page**************** 

@app.route('/test-url', methods=['POST'])
def test_url():
    nurl = request.json.get('testUrl')
    ourl = request.json.get('url')
    import os
    api_key = os.getenv("API_KEY")
    results = {}

    # Check VirusTotal report
    positives, total = get_virustotal_report(nurl, api_key)
    if positives is not None and total is not None:
        results['virus_total'] = f"Flagged {positives}/{total} times on VirusTotal."
    else:
        results['virus_total'] = "No VirusTotal report available."

    # Domain age check
    domain_age_result = check_domain_age(nurl)
    results['domain_age'] = domain_age_result

    # SSL certificate validation
    ssl_result = validate_ssl_certificate(nurl)
    results['ssl_certificate'] = ssl_result

    # Web scraping check (similarity score)
    original_html = scrape_url(ourl)
    log_function_start("scrape_url (suspicious_html)")
    suspicious_html = scrape_url(nurl)

    similarity_score = calculate_similarity(original_html, suspicious_html)
    results['web_scraping'] = f"Similarity score: {similarity_score:.2f}%"

    # similarity_score = calculate_similarity(original_html, suspicious_html)
    # results['web_scraping'] = f"Similarity score: {similarity_score:.2f}%"
    log_function_start("End Program")
    return jsonify(results)

@app.route('/predict-url', methods=['POST'])
def predict_url():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    # Extract features and format as a DataFrame
    features = extract_features(url)
    features_df = pd.DataFrame([features])

    # Make a prediction
    prediction = rf_classifier.predict(features_df)
    prediction_label = 0 if prediction[0] == 0 else 1

    return jsonify({'prediction': prediction_label})

@app.route('/fake-url-test', methods=['POST'])
def fake_test():

    url = request.json.get('url')
    import os
    api_key = os.getenv("API_KEY")

    results = {}


    # Check VirusTotal report
    positives, total = get_virustotal_report(url, api_key)
    if positives is not None and total is not None:
        results['virus_total'] = f"Flagged {positives}/{total} times on VirusTotal."
    else:
        results['virus_total'] = "No VirusTotal report available."

    # Domain age check
    domain_age_result = check_domain_age(url)
    results['domain_age'] = domain_age_result

    # SSL certificate validation
    ssl_result = validate_ssl_certificate(url)
    results['ssl_certificate'] = ssl_result
    log_function_start("End Program")
    return jsonify(results)


@app.route('/scrape-url', methods=['POST'])
def web_scrape_url():
    nurl = request.json.get('furl')
    ourl = request.json.get('ourl')
    results = {}

    # Web scraping check (similarity score)
    original_html = scrape_url(ourl)
    log_function_start("scrape_url (suspicious_html)")
    suspicious_html = scrape_url(nurl)

    # Check if either original_html or suspicious_html is None
    if original_html is None or suspicious_html is None:
        results['web_scraping'] = "Unable to retrieve content from one or both URLs."
    else:
        similarity_score = calculate_similarity(original_html, suspicious_html)
        results['web_scraping'] = f"Similarity score: {similarity_score:.2f}%"

    log_function_start("End Program")
    return jsonify(results)

    # similarity_score = calculate_similarity(original_html, suspicious_html)
    # results['web_scraping'] = f"Similarity score: {similarity_score:.2f}%"
    log_function_start("End Program")
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
