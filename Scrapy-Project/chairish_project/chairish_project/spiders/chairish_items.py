import scrapy
import re
from bs4 import BeautifulSoup
import json

class ChairishItemsSpider(scrapy.Spider):
    name = "chairish_items"
    allowed_domains = ["chairish.com"]
    # start_urls = ["https://chairish.com"]
    # seen_ids = set()

    cookies = {
        'csrftoken': '56t4uIp1yKIULiU6h4Z9ep9izTcbIe9m',
        'guid': '$10d864db-449c-4d63-958e-f64fc6588e47',
        '__utmz_chairish_02_11': '1745396779.utmcsr=google|utmcmd=organic|utmccn=(organic)|utmctr=(not%20provided)',
        'amplitude_id_1d2656bc9b05970f4174110ee401a478chairish.com': 'eyJkZXZpY2VJZCI6ImNmYThlZjlhLTI5YjEtNGJmYy05YjBkLTgxZmRjNjgxNDk0OFIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTc0NTY2MjE1NTU0OSwibGFzdEV2ZW50VGltZSI6MTc0NTY2MjM2Njg4OCwiZXZlbnRJZCI6MTIxLCJpZGVudGlmeUlkIjozMywic2VxdWVuY2VOdW1iZXIiOjE1NH0=',
        '_ga_2N8GB7SB99': 'GS1.1.1745662124.5.1.1745662362.0.0.0',
        '_ga': 'GA1.2.1970461985.1745396780',
        '_gcl_au': '1.1.1892184413.1745396780',
        '_attn_': 'eyJ1Ijoie1wiY29cIjoxNzQ1Mzk2Nzc5ODUyLFwidW9cIjoxNzQ1Mzk2Nzc5ODUyLFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcImFlODQ0YWRkY2FhNjQ2NzVhZDY1OWJkNGJkYTIwN2JjXCJ9Iiwic2VzIjoie1widmFsXCI6XCI2OWUzMjlkY2ExYzE0MjJkOTE0ZTZiNzgwMzcyMDc3MlwiLFwidW9cIjoxNzQ1NjYyMzYyMjM0LFwiY29cIjoxNzQ1NjYyMzYyMjM0LFwibWFcIjowLjAyMDgzMzMzMzMzMzMzMzMzMn0ifQ==',
        '__attentive_id': 'ae844addcaa64675ad659bd4bda207bc',
        '__attentive_cco': '1745396779852',
        '_pin_unauth': 'dWlkPU5URTFNVFF3TTJJdE56bGpOeTAwT0dNM0xUaGlPVFl0TkdSaVpUZG1OVEJsTkRKag',
        '__utma': '201483203.1970461985.1745396780.1745583515.1745662158.5',
        '__utmc': '201483203',
        '__utmz': '201483203.1745396781.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
        'tag_user_id': 'cec0c20e-a377-4215-833b-462d9910d64f-1745396779851',
        '_fbp': 'fb.1.1745396781848.554942937678278344',
        '_attn_bopd_': 'none',
        'fct': '1',
        'MCEvilPopupClosed': '1',
        '_gid': 'GA1.2.393390075.1745494601',
        '_ga_ETBJ2F4XFJ': 'GS1.1.1745497778.1.1.1745497973.0.0.0',
        '__attentive_dv': '1',
        '__attentive_session_id': '69e329dca1c1422d914e6b7803720772',
        '__utmb': '201483203.2.10.1745662158',
        '__utmt': '1',
        'tag_session': '4186a8c6-1dfb-4e87-a44a-f3a44d99df19-1f4d0683-8445-49aa-9e9a-ab086b115757',
        '__attentive_client_user_id': '$95ddd678-a297-47f5-9f40-3d56eec78a30',
        '__attentive_pv': '2',
        '__attentive_ss_referrer': 'ORGANIC',
        '_uetsid': '62787560210011f0b954993f3d8d4ccb',
        '_uetvid': 'a1f1da70201c11f095545d10590a6661',
        'sailthru_pageviews': '1',
        'sailthru_content': 'aa38bf6fd3d6af8e1890d9a8a49cbc647b2fafd0367bce54ea3bea21db16a06dde22fc48f821438a3f93e3e24c07441d37fe0198ae66e7c6e1357ba9c1d3426bbb8239aff217f6073ee28b5bcfa40d2318847a78b0c4eaaa50fa3ca09635173d',
        'sailthru_visitor': '9f3bc605-8b43-419d-b92e-004ca5464b01',
        'PLPopupClosed': '1',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': 'https://www.chairish.com/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Priority': 'u=0, i',
    }

    def start_requests(self):

        url = 'https://www.chairish.com/collection/doors?q=doors'
        yield scrapy. Request(url, method='get', callback=self.list_info, cookies=self.cookies, headers=self.headers)

    def list_info (self, response):
        soup = BeautifulSoup(response.text,'html.parser')
        main_script = ''
        json_data = None
        for script in soup.find_all('script'):

            if 'context.PRODUCT_ID_TO_PRODUCT_JSON_MAP' in script.text:
                main_script = script.text
                break

        if main_script:
            json_match = re.search("context.PRODUCT_ID_TO_PRODUCT_JSON_MAP = ({.*?});", main_script)
        if json_match:
            json_data = json.loads(json_match.group(1))
        else:
            json_data ={}

        if json_data.items():
            for key, value in json_data.items():
                prod_name =  value.get("title")
                pro_link = 'https://www.chairish.com' + value.get('url')
                price = value.get('your_price').get('current').get('value')
                display	 = value.get('your_price').get('current').get('display')
                verbose	 = value.get('your_price').get('current').get('verbose')
                prod_id = value.get('id')

                yield {
                    "id": prod_id,
                    "prod_name": prod_name,
                    "price": price,
                    "display": display,
                    "verbose": verbose,
                    "pro_link": pro_link
                    }
           
        pagin = soup.find('li','next')   
        print(pagin,'     ======================')
        if pagin:
            next_page = 'https://www.chairish.com' + pagin.find('a').get('href')
            if next_page:
                print('======================----------',next_page)
                yield scrapy.Request(next_page, method='get', callback= self.list_info, cookies=self.cookies, headers=self.headers)



    # scrapy crawl chairish_items -o chairish_results.xlsx
