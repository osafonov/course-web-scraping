import json
import os
import re
import urllib.parse
from multiprocessing.dummy import Pool

import requests
from bs4 import BeautifulSoup


def get_content(url):
    result = re.search('http(s|\s):\/\/(.+)', url)
    file_name = result.group(2).replace('/', '_')

    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            content = f.read()
        return content

    response = requests.get(
        url=url,
        headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
    )
    with open(file_name, 'w') as f:
        f.write(response.text)
    return response.text


def get_related_topics_from_page(page_url):
    content = get_content(page_url)

    soup = BeautifulSoup(content, 'lxml')

    topic_tags = soup.select('[data-component="topic-list"] a')
    topics = [topic.text for topic in topic_tags]

    return {'url': page_url, 'topics': topics}


def parse_asynch():
    url = 'https://www.bbc.com/sport'
    content = get_content(url)

    soup = BeautifulSoup(content, features='lxml')

    data = []

    blocks = soup.select('[type=article] a[class*=PromoLink]', limit=5)
    urls = [urllib.parse.urljoin(url, block.get('href').strip()) for block in blocks]

    print(urls)

    with Pool(5) as p:
        data = p.map(get_related_topics_from_page, urls)

    with open('asynch_hw.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    parse_asynch()