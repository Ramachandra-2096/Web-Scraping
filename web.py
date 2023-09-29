import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os

# URL of the website you want to scrape
url = "https://www.facebook.com/"

# Create a folder named "assets" if it doesn't exist
assets_folder = "assets"
if not os.path.exists(assets_folder):
    os.makedirs(assets_folder)

try:
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract HTML code
        html_code = soup.prettify()

        # Initialize lists for CSS and JavaScript URLs
        css_urls = []
        js_urls = []

