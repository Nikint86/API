import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


SHORTEN_LINK_URL = 'https://api.vk.com/method/utils.getShortLink'
LINK_STATS_URL = 'https://api.vk.com/method/utils.getLinkStats'


def shorten_link(token, url):
    payload = {
        "access_token": token,
        "v": "5.199",
        "url": url,
        "private": "0"
    }
    response = requests.get(SHORTEN_LINK_URL, params=payload)
    response.raise_for_status()
    request_response = response.json()
    return request_response['response']['short_url']


def count_clicks(token, short_url):
    parsed = urlparse(short_url)
    path = parsed.path.strip('/')
    payload = {
        "access_token": token,
        "v": "5.199",
        "url": short_url,
        "interval": 'forever',
        "private": "0",
        "key": path
    }
    response = requests.get(LINK_STATS_URL, params=payload)
    response.raise_for_status()
    stats = response.json()
    return stats['response']['stats'][0]['views']


def is_short_link(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc == 'vk.cc'


def main():
 load_dotenv()
 token = os.environ["VK_TOKEN"]
 url_input = input("Введите ссылку: ")
 try:
    if is_short_link(url_input):
        clicks = count_clicks(token, url_input)
        print('Количество просмотров:', clicks)
    else:
        short_link = shorten_link(token, url_input)
        print('Сокращенная ссылка:', short_link)
 except requests.exceptions.HTTPError as e:
    print("Ошибка при запросе:", str(e))


if __name__ == "__main__":
    main()



