import re

import scrapy
from scrapy import Request

import random


def get_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.3',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.3',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.',
        'Mozilla/5.0 (Windows NT 6.1; rv:109.0) Gecko/20100101 Firefox/115.',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.120 Safari/537.36 Avast/109.0.24252.12',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.'
    ]
    return random.choice(user_agents)


class A1893Spider(scrapy.Spider):
    name = "1893"
    allowed_domains = ["www.1893-wohnen.de"]
    start_urls = ["https://www.1893-wohnen.de/en/wohnungen/"]

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'USER_AGENT': get_user_agent()
    }

    def parse(self, response):
        links = response.css('.result-item a')
        for link in links:
            url = link.attrib['href']
            yield Request(url, callback=self.parse_ad)

    def parse_ad(self, response):
        id = response.url.split('=')[1]
        url = response.url

        # section = response.css('.section__rent:nth-of-type(1)')
        section = response.xpath("//*[contains(@class,'section__rent')][1]")
        title = section.css('h2::text').get()
        subtitle = section.css('.subtitle-text::text').get()
        address = subtitle.split('/')[0] + ', ' + subtitle.split('/')[1]
        floor = re.findall(r'\d', subtitle.split('/')[2])[0]
        price = re.findall(r'\d.', response.xpath("//*[contains(@class,'col')][3]//strong/text()").get())[0]
        rooms = re.findall(r'\d', response.xpath("//*[contains(@class,'col')][1]//strong/text()").get().split('/')[0])[0]
        size = re.findall(r'\d.', response.xpath("//*[contains(@class,'col')][1]//strong/text()").get().split('/')[1])[0]
        full_text = response.css('.rent-advantages::text').get() + '\n' + response.css('.rent-params::text').get()

        yield {
            'source': {
                'name': self.name,
                'url': self.start_urls[0]
            },
            'company': {
                'name': self.name
            },
            'ad': {
                'id': id,
                'url': url,
                'title': title,
                'address': address,
                'price': price,
                'rooms': rooms,
                'floor': floor,
                'size': size,
                'full_text': full_text,
                'date': None
            }
        }
