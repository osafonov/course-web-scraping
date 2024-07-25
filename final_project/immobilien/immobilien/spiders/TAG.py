import requests
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


class TagSpider(scrapy.Spider):
    name = "TAG"
    allowed_domains = ["tag-wohnen.de"]
    start_urls = ["https://tag-wohnen.de/immosuche?filters%5Bproperty_city%5D[]=Eberswalde&size=100&view=LIST"]

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'USER_AGENT': get_user_agent()
    }

    def parse(self, response):
        response = requests.get(
            url='https://immo.isp-10130-1.domservice.de/properties?filters%5Bproperty_city%5D[]=Eberswalde&size=100&view=LIST',
            headers={'User-Agent': get_user_agent()}
        )
        results = response.json()['response']['results']

        for result in results:
            url = "https://tag-wohnen.de/immosuche/expose?object_id=" + result['id'].replace('/', '%2F')
            yield Request(
                url,
                callback=self.parse_ad,
                headers={'User-Agent': get_user_agent()},
                meta={"id": result['id'], "data": result['extrnal_updated_at'], "cookies": response.cookies}
            )

    def parse_ad(self, response):
        id = response.meta['id']
        url = response.url

        response_get = requests.get(
            url='https://immo.isp-10130-1.domservice.de/properties/' + id.replace('/', '%2F'),
            headers={'User-Agent': get_user_agent()},
            cookies=response.meta['cookies']
        )

        property = response_get.json()['property']

        title = property['title']
        address = f"{property['street']}, {property['property_zip']} {property['property_city']}"
        price = property['overall_warm']
        rooms = property['number_of_rooms']
        floor = property['level']
        size = property['living_space']
        full_text = f"{property['description']}\n{property['location_description']}\n{property['features_description']}"

        # title = response.xpath('//h1/text()')
        # address = response.xpath("//*[@class='expose-header__kicker']/text()").get()
        # price = re.findall(r'\d.', response.xpath("//*[contains(@class, 'box-rent__list-content--highlighted')]/text()").get())[0]
        # rooms = response.xpath("//header//*[contains(text(), 'Zimmer')]/following-sibling::dd/text()")
        # floor = response.xpath("//*[contains(text(), 'Etage')]/following-sibling::td/text()")
        # size = re.findall(r'\d.', response.xpath("//header//*[contains(text(), 'Wohnfläche')]/following-sibling::dd/text()"))[0]
        # full_text = response.css('.article-content__block .text::text')

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
                'date': response.meta['data']
            }
        }

