# dynamic_analyzer.py

import ssl
import socket
import requests
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def get_redirect_chain(url):
    """
    Follows HTTP redirects using requests to get the full redirect chain.
    """
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        return [resp.url for resp in response.history] + [response.url]
    except requests.RequestException:
        return [url]

def get_ssl_certificate_info(url):
    """
    Fetch SSL certificate details.
    """
    try:
        hostname = urlparse(url).hostname
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                return cert
    except Exception:
        return None

def analyze_url(url):
    """
    Analyzes a given URL by visiting it in a headless browser and
    extracting key information.
    """
    print(f"[*] Starting dynamic analysis for URL: {url}")

    # Collect redirect chain using requests
    redirect_chain = get_redirect_chain(url)

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Create WebDriver instance
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    analysis_data = {
        "initial_url": url,
        "final_url": redirect_chain[-1],
        "redirect_chain": redirect_chain[:-1],
        "page_title": None,
        "page_source": None,
        "has_login_form": False,
        "ssl_certificate_info": get_ssl_certificate_info(redirect_chain[-1])
    }

    try:
        # Navigate to the final URL
        driver.get(analysis_data["final_url"])

        # Wait for page to load
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )

        # Capture page title and source
        analysis_data["page_title"] = driver.title
        page_source = driver.page_source
        analysis_data["page_source"] = page_source

        # Analyze content using BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Detect login forms (username/email + password input)
        forms = soup.find_all('form')
        for form in forms:
            has_password = form.find('input', {'type': 'password'})
            has_username = form.find('input', {'type': 'text'}) or form.find('input', {'type': 'email'})
            if has_password and has_username:
                analysis_data["has_login_form"] = True
                break

    except Exception as e:
        print(f"[!] An error occurred during analysis: {e}")

    finally:
        driver.quit()
        print("[*] Analysis complete. Browser closed.")

    return analysis_data

# Example Usage:
if __name__ == "__main__":
    test_url = "https://www.google.com"
    results = analyze_url(test_url)
    if results:
        print("\n--- Analysis Results ---")
        print(f"Initial URL: {results['initial_url']}")
        print(f"Final URL: {results['final_url']}")
        print(f"Redirects: {results['redirect_chain']}")
        print(f"Page Title: {results['page_title']}")
        print(f"Login Form Detected: {results['has_login_form']}")
        print(f"SSL Certificate Info: {results['ssl_certificate_info']}")
