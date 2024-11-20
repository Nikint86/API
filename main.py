import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()
token = os.getenv("TOKEN")

shorten_link_url = 'https://api.vk.com/method/utils.getShortLink'
link_stats_url = 'https://api.vk.com/method/utils.getLinkStats'

def shorten_link(token, url):
    payload = {
        "access_token": token,
        "v": "5.199",
        "url": url,
        "private": "0"
    }
    response = requests.get(shorten_link_url, params=payload)
    response.raise_for_status()
    new_side = response.json()
    return new_side['response']['short_url']

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
    response = requests.get(link_stats_url, params=payload)
    response.raise_for_status()
    stats = response.json()
    return stats['response']['stats'][0]['views']

def is_short_link(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc == 'vk.cc'

def process_user_input():
 url_fut_side = input("Введите ссылку: ")
 try:
    if is_short_link(url_fut_side):
        clicks = count_clicks(token, url_fut_side)
        print('Количество просмотров:', clicks)
    else:
        short_link = shorten_link(token, url_fut_side)
        print('Сокращенная ссылка:', short_link)
 except requests.exceptions.HTTPError as e:
    print("Ошибка при запросе:", str(e))

if __name__ == "__main__":
    process_user_input()



#"dvmn.org/modules"

"https://dvmn.org/modules/web-api/lesson/vk-short-link/#8"