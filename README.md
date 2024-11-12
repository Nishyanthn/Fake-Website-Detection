<h1 align="center"> ⚠️ Fake Website Detection 💻❗</h1>
<h3 align="left">
🔴The Fake Website Detection System is a robust application designed to assess the legitimacy of websites by analyzing various indicators of authenticity. This system is particularly useful for users who wish to verify the safety of URLs they encounter, either through a comprehensive scan of suspicious variants of a known URL or through a direct analysis of a potentially suspicious URL provided by the user. The application combines several detection techniques, leveraging both real-time web data and machine learning models to deliver accurate results.

Key Features and Methods:
URL Generation and Suspicious URL Scanning:

🔴Typo-Squatting and Homoglyph Variations: Upon receiving an original URL, the system generates a list of similar-looking URLs using typos, homoglyphs, and different TLDs (Top-Level Domains). This step is useful for detecting potential phishing attempts where malicious websites use URLs resembling legitimate ones.
Live URL Detection: Each generated URL is tested to see if it is live on the internet, filtering out inactive URLs and focusing the scan on potentially active threats.
Domain Age Check:

🔴The domain age is retrieved to verify the credibility of the website. Generally, legitimate businesses have older domains, whereas malicious websites tend to be relatively new. This feature helps in identifying potentially risky domains based on their creation dates.
SSL Certificate Validation:

🔴The system checks if a valid SSL certificate is present, which is crucial for website security. Websites without SSL certificates or with expired/invalid certificates may pose a higher risk, as legitimate sites generally prioritize SSL security.
VirusTotal API Integration:

🔴Using the VirusTotal API, the system scans the provided URL against a vast database of known malicious sites. If the URL is flagged by VirusTotal, it provides an indication of previous reports of suspicious activity related to that domain.
Content-Based Similarity Scoring via Web Scraping:

🔴The application scrapes the HTML content of both the original and the suspicious URLs and calculates a similarity score using content comparison algorithms. This score indicates how closely a suspicious URL mirrors the content of the original website, which can help identify sites that imitate legitimate pages for phishing.
Machine Learning (ML) Model Prediction:

🔴A trained Random Forest Classifier model is incorporated to further evaluate the legitimacy of the website. The ML model uses extracted features (such as domain age, SSL presence, and VirusTotal findings) to predict whether a URL is likely to be legitimate or fake. This predictive analysis is based on historical data of legitimate and fake websites, enabling a more refined classification.
Two-Step User Flow:

🔴The system has two main modes:
Scan Mode: Takes an original URL as input, generates multiple suspicious variations, and evaluates each for legitimacy, displaying the results in a detailed report.
Direct URL Validation Mode: Allows users to enter a URL they suspect might be malicious. This mode bypasses the URL generation step and directly runs all the tests on the provided URL.</h3>


<p align="left">
</p>

<h3 align="left">Languages and Tools:</h3>
<p align="left"> <a href="https://www.w3schools.com/css/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg" alt="css3" width="40" height="40"/> </a> <a href="https://www.docker.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a> <a href="https://flask.palletsprojects.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/pocoo_flask/pocoo_flask-icon.svg" alt="flask" width="40" height="40"/> </a> <a href="https://www.w3.org/html/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/> </a> <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="javascript" width="40" height="40"/> </a> <a href="https://nodejs.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nodejs/nodejs-original-wordmark.svg" alt="nodejs" width="40" height="40"/> </a> <a href="https://pandas.pydata.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/2ae2a900d2f041da66e950e4d48052658d850630/icons/pandas/pandas-original.svg" alt="pandas" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> <a href="https://reactjs.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/react/react-original-wordmark.svg" alt="react" width="40" height="40"/> </a> <a href="https://scikit-learn.org/" target="_blank" rel="noreferrer"> <img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg" alt="scikit_learn" width="40" height="40"/> </a> <a href="https://www.selenium.dev" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/detain/svg-logos/780f25886640cef088af994181646db2f6b1a3f8/svg/selenium-logo.svg" alt="selenium" width="40" height="40"/> </a> </p>
