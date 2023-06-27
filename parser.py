import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_list_of_sushi(url):
    html = requests.get(url)
    soup = BeautifulSoup(html, "html5lib")

    pictures = []
    for i in soup.select(".next-image-wrapper > img"):
        url = i.get("src")

        parsed_url = urlparse(url)
        new_url = parsed_url._replace(query='').geturl()

        pictures.append(new_url)

    text = []
    for data in soup.select('.bottom-block'):
        text.append(data.text)

    zipped_data = list(zip(pictures, text))
    print(zipped_data)
    return zipped_data
