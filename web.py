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
        # Find and extract CSS links from <link> tags
        link_tags = soup.find_all("link", rel="stylesheet")
        for link_tag in link_tags:
            css_url = link_tag.get("href")
            if css_url:
                css_urls.append(urljoin(url, css_url))

        # Find and extract JavaScript URLs from <script> tags
        script_tags = soup.find_all("script", src=True)
        for script_tag in script_tags:
            js_url = script_tag.get("src")
            if js_url:
                js_urls.append(urljoin(url, js_url))

        # Retrieve CSS content
        css_code = ""
        for css_url in css_urls:
            css_response = requests.get(css_url)
            if css_response.status_code == 200:
                css_code += f"/* CSS from {css_url} */\n"
                css_code += css_response.text + "\n"

        # Retrieve JavaScript content
        js_code = ""
        for js_url in js_urls:
            js_response = requests.get(js_url)
            if js_response.status_code == 200:
                js_code += f"/* JavaScript from {js_url} */\n"
                js_code += js_response.text + "\n"

        # Save the extracted code to text files
        with open("index.html", "w", encoding="utf-8") as html_file:
            html_file.write(html_code)

        with open("style.css", "w", encoding="utf-8") as css_file:
            css_file.write(css_code)

        with open("script.js", "w", encoding="utf-8") as js_file:
            js_file.write(js_code)

        print("HTML, CSS, and JavaScript code saved to text files.")
        # Retrieve and save images
        img_tags = soup.find_all("img")
        for img_tag in img_tags:
            img_url = img_tag.get("src")
            if img_url:
                img_url = urljoin(url, img_url)
                img_response = requests.get(img_url)
                if img_response.status_code == 200:
                    img_name = os.path.join(
                        assets_folder, os.path.basename(urlparse(img_url).path)
                    )
                    with open(img_name, "wb") as img_file:
                        img_file.write(img_response.content)
                    print(f"Image saved: {img_name}")

    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)

except requests.exceptions.RequestException as e:
    print("An error occurred:", str(e))

