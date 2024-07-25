import requests
import scrapy

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


class WhgSpider(scrapy.Spider):
    name = "WHG"
    allowed_domains = ["www.whg-ebw.de"]
    start_urls = ["https://www.whg-ebw.de/"]
    rest_base_url = 'https://asp1.immosolve.eu/immosolve2/api/rest/hpm/estates/'

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'USER_AGENT': get_user_agent()
    }

    def parse(self, response):
        # body = '{"presentationId":"e6fc8ce107f2bdf0955f021a391514ce","mandatorId":"d8c0596fc302d312bb4426bbb97079fb","objectIdentifier":2,"allowedObjectIdentifiers":[2],"calendarData":true,"city":null,"chosenLocation":null,"radius":null,"minimumLocation":null,"maximumLocation":null,"regions":[1,2,3,4,5,6,7,8,9,10,11],"personCount":null,"dateStart":null,"dateEnd":null,"roomsStart":null,"roomsEnd":null,"priceStart":null,"priceEnd":null,"areaStart":null,"areaEnd":null,"floor":null,"specialties":[],"userCode":null,"elementsPerPage":2000,"currentPage":1,"orderBy":null,"objectId":null,"objectCode":null,"category":null}'
        # body = '{"presentationId":"e6fc8ce107f2bdf0955f021a391514ce","mandatorId":"d8c0596fc302d312bb4426bbb97079fb","objectIdentifier":2,"allowedObjectIdentifiers":[2],"calendarData":true,"regions":[1,2,3,4,5,6,7,8,9,10,11],"specialties":[],"elementsPerPage":2000,"currentPage":1}'
        # body = '{"objectIdentifier":2,"allowedObjectIdentifiers":[2],"regions":[1],"elementsPerPage":200,"currentPage":1}'
        body = '{"presentationId":"e6fc8ce107f2bdf0955f021a391514ce","mandatorId":"d8c0596fc302d312bb4426bbb97079fb","objectIdentifier":2,"allowedObjectIdentifiers":[2],"calendarData":true,"regions":[1,3,4,5,6],"elementsPerPage":2000,"currentPage":1}'
        response = requests.post(
            # url=self.rest_base_url + 'list',
            url='https://asp1.immosolve.eu/immosolve2/api/rest/hpm/estates/list',
            # headers={
            #     'User-Agent': get_user_agent(),
            #     'content-type': 'application/json; charset=UTF-8',
            #     'accept': 'application/json, text/plain, */*',
            #     'accept-encoding': 'gzip, deflate, br, zstd',
            #     'accept-language': 'en-US,en;q=0.9,de-DE;q=0.8,de;q=0.7,uk-UA;q=0.6,uk;q=0.5',
            #     'connection': 'keep-alive',
            #     'content-length': f'{len(body)}',
            #     'Host': 'asp1.immosolve.eu',
            #     'origin': 'https://2161148.hpm.immosolve.eu',
            #     'Referer': 'https://2161148.hpm.immosolve.eu/',
            #     'Sec-Fetch-Dest': 'empty',
            #     'Sec-Fetch-Mode': 'cors',
            #     'Sec-Fetch-Site': 'same-site'
            # },
            headers={
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9,de-DE;q=0.8,de;q=0.7,uk-UA;q=0.6,uk;q=0.5',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json; charset=UTF-8',
                'Origin': 'https://2161148.hpm.immosolve.eu',
                'Referer': 'https://2161148.hpm.immosolve.eu/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': "Linux",
                'Content-Length': '{len(body)}',
                'Cache-Control': 'no-cache',
                'Accept-Encoding': 'gzip, deflate, br',
                # 'Cookie': 'JSESSIONID=6E18FDB38C84030C699D2DB195A1A658; AWSELB=1332441098.20480.0000'
            },
            cookies={'JSESSIONID': '6E18FDB38C84030C699D2DB195A1A658', 'AWSELB': '1332441098.20480.0000',},
            json=body
        )
        results = response.json()['immoObjects']

        for result in results:
            id = result['id']
            response = requests.post(
                url=self.rest_base_url + "details",
                headers={'User-Agent': get_user_agent()},
                json=f'{"presentationId":"e6fc8ce107f2bdf0955f021a391514ce","mandatorId":"d8c0596fc302d312bb4426bbb97079fb","id":"{id}"}'
            )
            labels = response.json()['immoObject']['labels']
            description = response.json()['descriptions']

            title = labels['title']
            address = f"{labels['strasse']}, {property['plz']} {property['ort']}"
            price = labels['monatlGesamtkosten'].replace('.','')
            rooms = labels['anzahlGanzeZimmer']
            floor = labels['etageValue']
            size = labels['wohnflaeche']
            full_text = f"{description['ausstattungsbeschreibung']}\n{description['objektbeschreibung']}\n{description['sonstiges']}"

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
                    'url': response.url,
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


# def get_user_agent():
#     user_agents = [
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.3',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.3',
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.',
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.',
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.',
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3',
#         'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.3',
#         'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.',
#         'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.',
#         'Mozilla/5.0 (Windows NT 6.1; rv:109.0) Gecko/20100101 Firefox/115.',
#         'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.120 Safari/537.36 Avast/109.0.24252.12',
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.'
#     ]
#     return random.choice(user_agents)
