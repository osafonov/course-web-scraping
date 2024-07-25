import re

import scrapy
import random

from scrapy import Request


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


class KleinanzeigenSpider(scrapy.Spider):
    name = "kleinanzeigen"
    allowed_domains = ["www.kleinanzeigen.de"]
    start_urls = [
        "https://www.kleinanzeigen.de/s-wohnung-mieten/16227/preis::1000/c203l7722+wohnung_mieten.qm_d:65%2C+wohnung_mieten.zimmer_d:3%2C4"]

    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'USER_AGENT': get_user_agent()
    }
    base_url = 'https://asp1.immosolve.eu/immosolve2/api/rest/hpm/estates/'

    def parse(self, response):
        links = response.css('#srchrslt-adtable article h2>a')
        for link in links:
            url = self.base_url + link.attrib['href']
            yield Request(url, callback=self.parse_ad)

    def parse_ad(self, response):
        parts = response.url.split('/')
        id = parts[len(parts - 1)]
        url = response.url

        title = response.css('#viewad-title::text').get()
        address = response.css('#vviewad-locality::text').get()
        date = response.css('#viewad-extra-info span::text').get()
        price = re.findall(r'\d.', response.css("#viewad-price::text").get())[0]
        full_text = response.css('.viewad-description-text::text').get()

        details_section = response.css('#viewad-details').get()
        floor = details_section.xpath('li[contains(text(),"Etage")/span/text()]').get()
        rooms = details_section.xpath('li[contains(text(),"Zimmer")/span/text()]').get()
        size = re.findall(r'\d.', details_section.xpath('li[contains(text(),"Wohnfläche")/span/text()]').get())[0]

        contact = response.css('#viewad-contact .userprofile-vip a::text').get()

        yield {
            'source': {
                'name': self.name,
                'url': self.start_urls[0]
            },
            'company': {
                'name': contact
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
                'date': date
            }
        }
