import json
import os.path
import re
from time import time

import requests
from bs4 import BeautifulSoup
from multiprocess.dummy import Pool


def parse_xml():
    xml = """
        <library>
            <book>
                <title>Great Title</title>
                <author>Rey Bray</author>
                <year>2003</year>
                <isbn>123456-7890</isbn>
            </book>
            <book>
                <title>Groovy</title>
                <author>Guy Boovy</author>
                <year>2021</year>
                <isbn>000456-7890</isbn>
            </book>
            <book>
                <title>Java for dummies</title>
                <author>Author J.r</author>
                <year>2024</year>
                <isbn>110456-7111</isbn>
            </book>
        </library>
    """

    soup = BeautifulSoup(xml, features='xml')

    book = soup.find('book')
    # print(book)

    element = soup.find(string='Java for dummies')
    # print(element.parent.parent)

    book_titles = soup.find_all('title', string=re.compile("Java|Groovy"))
    # print(book_titles)

    titles = soup.find_all('title')
    titles = [tag.text for tag in titles]

    years = [tag.text for tag in soup.find_all('year')]

    for title, year in zip(titles, years):
        print(f'The book {title} was written in {year}')


def parse_html():
    url = 'https://job.morion.ua/jobs/'
    content = get_content(url)

    soup = BeautifulSoup(content, features='lxml')

    data = []

    blocks = soup.find_all('h3')
    blocks = [block.parent for block in blocks if block.get('class') is None]

    print(len(blocks))

    for block in blocks:
        title = block.find('h3').text.strip()
        url = block.find('h3').find('a').get('href').strip()
        salary_tag = block.find('p', {'class': 'salary-city__vacancy'})
        salary = salary_tag.text.strip() if salary_tag else ''

        data.append({'title': title, 'url': url, 'salary': salary})

    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def parse_page(page_url):
    content = get_content(page_url)

    soup = BeautifulSoup(content, 'lxml')

    site = soup.find('dt', string='Сайт:').find_next_sibling('dd').find('a').text.strip()

    return {'url': page_url, 'site': site}


def parse_synch():
    url = 'https://job.morion.ua/jobs/'
    content = get_content(url)

    soup = BeautifulSoup(content, features='lxml')

    data = []

    blocks = soup.find_all('h3')
    blocks = [block.parent for block in blocks if block.get('class') is None]

    for block in blocks:
        url = block.find('h3').find('a').get('href').strip()
        page_data = parse_page(url)
        data.append(page_data)

    with open('synch.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def parse_asynch():
    url = 'https://job.morion.ua/jobs/'
    content = get_content(url)

    soup = BeautifulSoup(content, features='lxml')

    data = []

    blocks = soup.find_all('h3')
    blocks = [block.parent for block in blocks if block.get('class') is None]
    urls = [block.find('h3').find('a').get('href').strip() for block in blocks]

    print(urls)

    with Pool(5) as p:
        data = p.map(parse_page, urls)

    with open('asynch.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_content(url):
    result = re.search('http(s|\s):\/\/(.+)', url)
    file_name = result.group(2).replace('/', '_')

    # if os.path.exists(file_name):
    #     with open(file_name, 'r') as f:
    #         content = f.read()
    #     return content

    response = requests.get(
        url=url,
        headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
    )
    with open(file_name, 'w') as f:
        f.write(response.text)
    return response.text


def explain_map():
    add = lambda x, y: x + y
    items = [(1, 3, 5), (2, 4, 6)]
    results = map(add, *items)
    print(list(results))


if __name__ == '__main__':
    # parse_xml()
    # parse_html()

    # start = time()
    # parse_synch()
    # finish = time()
    # print(finish - start)  # 12.57

    # explain_map()

    start = time()
    parse_asynch()
    finish = time()
    print(finish - start)  # 3.2
