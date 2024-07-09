import base64
import argparse
from bs4 import BeautifulSoup
from urllib.parse import unquote

# Command-line arguments
parser = argparse.ArgumentParser(description="Get URLs from a EML file")
parser.add_argument("--filename", type=str)
args = parser.parse_args()
filename = args.filename

# Constants
outlook_safelinks = 'https://emea01.safelinks.protection.outlook.com/?url='

urls = []

def get_html_from_eml_file(filename):
    with open(filename, "r") as eml_file:
        lines = eml_file.readlines()

    count = 0

    for line in lines:
        count += 1
        if "text/html" in line:
            break

    encoded_html = lines[count+3]
    eml_file.close()

    return base64.b64decode(encoded_html)

# Extract URLs from a elements
def get_urls_from_a(soup):
    for link in soup.find_all('a', href=True):
        url = str(link.get('href'))

        # Remove outlook's safelinks if it is present
        if outlook_safelinks in url:
            url = url.replace(outlook_safelinks,'')
            url = unquote(url)
            url_info = dict(element = '<a>', url = url)
        urls.append(url_info)

# Extract URLs from img elements
def get_urls_from_img(soup):
    for link in soup.find_all('img'):
        url = str(link.attrs['src'])
        url_info = dict(element = '<img>', url = url)
        urls.append(url_info)

def print_urls():
    for url in urls:
        print(f'From {url["element"]} element:\n{url["url"]}\n')

def main():
    # Parse HTML
    html = get_html_from_eml_file(filename)
    soup = BeautifulSoup(html, "html.parser")

    get_urls_from_a(soup)
    get_urls_from_img(soup)
    print_urls()

if __name__ == "__main__":
    main()
