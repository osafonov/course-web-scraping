import requests
import re


def use_get():
    response = requests.get('https://www.lejobadequat.com/emplois')
    print('Status code: ', response.status_code)
    print('Content HTML: ', response.text)


def use_post():
    payload = {"action": "facetwp_refresh",
               "data": {"facets": {"recherche": [], "ou": [], "type_de_contrat": [], "fonction": [], "load_more": [2]},
                        "frozen_facets": {"ou": "hard"}, "http_params": {"get": [], "uri": "emplois", "url_vars": []},
                        "template": "wp", "extras": {"counts": True, "sort": "default"}, "soft_refresh": 1,
                        "is_bfcache": 1, "first_load": 0, "paged": 2}}
    response = requests.post('https://www.lejobadequat.com/emplois', json=payload)
    print('Status code: ', response.status_code)
    print('Content: ', response.json()['template'])


def get_user_agent():
    pattern = ''
    response = requests.post('https://www.whatismybrowser.com/what-http-headers-is-my-browser-sending/')
    print('Status code: ', response.status_code)
    print('Content: ', response.text)


def use_proxy():
    response = requests.get('https://2ip.io/')
    print(response.text)

    proxy = '162.254.190.106'
    port = 31280

    proxies = {
        'http': f'http://{proxy}:{port}',
        'https': f'https://{proxy}:{port}'
    }

    # response = requests.get('https://2ip.io/', proxies=proxies)
    print(response.text)


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
    # use_proxy()
    get_content('https://www.whatismybrowser.com/what-http-headers-is-my-browser-sending/')
