import requests
import re
import json
import sqlite3
import lxml
from pprint import pprint
from bs4 import BeautifulSoup


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
        </library>
    """

    soup = BeautifulSoup(xml, features='xml')
    print(soup.find_all('book'))


def parse_html():
    url = 'https://job.morion.ua/jobs/'
    content = get_content(url)

    soup = BeautifulSoup(content, features='lxml')

    data = []

    blocks = soup.find_all('h3')
    blocks = [block.parent for block in blocks if block.get('class') is None]




    print(blocks)







def get_content(url):
    result = re.search('http(s|\s):\/\/(.+)', url)
    file_name = result.group(2).replace('/', '_')
    try:
        with open(file_name, 'r') as f:
            content = f.read()
            return content
    except:
        response = requests.get(url)
        with open(file_name, 'w') as f:
            f.write(response.text)
        return response.text



if __name__ == '__main__':
    # get_vacancies()
    # parse_xml()
    parse_html()
