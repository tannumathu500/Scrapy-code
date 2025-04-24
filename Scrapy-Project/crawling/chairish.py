import requests
from bs4 import BeautifulSoup
import json
import re

cookies = {
    'csrftoken': 'l5IujLDZWrKb8gszAoef6slI3Q8K9Pia',
    'guid': '$d4c418c8-f118-4f2c-b28c-8843407b47e4',
    '__utmz_chairish_02_11': '1745396779.utmcsr=google|utmcmd=organic|utmccn=(organic)|utmctr=(not%20provided)',
    'amplitude_id_1d2656bc9b05970f4174110ee401a478chairish.com': 'eyJkZXZpY2VJZCI6ImNmYThlZjlhLTI5YjEtNGJmYy05YjBkLTgxZmRjNjgxNDk0OFIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTc0NTQ5NDU4NTExNSwibGFzdEV2ZW50VGltZSI6MTc0NTQ5NDYzMDI0MywiZXZlbnRJZCI6ODQsImlkZW50aWZ5SWQiOjI1LCJzZXF1ZW5jZU51bWJlciI6MTA5fQ==',
    '_ga_2N8GB7SB99': 'GS1.1.1745494596.2.1.1745494598.0.0.0',
    '_ga': 'GA1.2.1970461985.1745396780',
    '_gcl_au': '1.1.1892184413.1745396780',
    '_attn_': 'eyJ1Ijoie1wiY29cIjoxNzQ1Mzk2Nzc5ODUyLFwidW9cIjoxNzQ1Mzk2Nzc5ODUyLFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcImFlODQ0YWRkY2FhNjQ2NzVhZDY1OWJkNGJkYTIwN2JjXCJ9Iiwic2VzIjoie1widmFsXCI6XCJhYzRiMjI2ZTBhZmM0MWNiYTBkNzJmYWMxOGZmOWUxMFwiLFwidW9cIjoxNzQ1NDk0NTk4MzE1LFwiY29cIjoxNzQ1NDk0NTk4MzE1LFwibWFcIjowLjAyMDgzMzMzMzMzMzMzMzMzMn0ifQ==',
    '__attentive_id': 'ae844addcaa64675ad659bd4bda207bc',
    '__attentive_cco': '1745396779852',
    '_pin_unauth': 'dWlkPU5URTFNVFF3TTJJdE56bGpOeTAwT0dNM0xUaGlPVFl0TkdSaVpUZG1OVEJsTkRKag',
    '__utma': '201483203.1970461985.1745396780.1745396781.1745494598.2',
    '__utmc': '201483203',
    '__utmz': '201483203.1745396781.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
    'tag_user_id': 'cec0c20e-a377-4215-833b-462d9910d64f-1745396779851',
    '_fbp': 'fb.1.1745396781848.554942937678278344',
    '_attn_bopd_': 'none',
    'fct': '0',
    'MCEvilPopupClosed': '1',
    '__utmb': '201483203.1.10.1745494598',
    '__utmt': '1',
    '__attentive_session_id': 'ac4b226e0afc41cba0d72fac18ff9e10',
    '_uetsid': '62787560210011f0b954993f3d8d4ccb',
    '_uetvid': 'a1f1da70201c11f095545d10590a6661',
    'tag_session': '5caf641b-4750-4013-8632-92e093dc1b30-2ea2830f-e975-4d67-b880-927673ae3ab6',
    'sailthru_pageviews': '1',
    '__attentive_client_user_id': '$0e5044e4-8b9e-47da-b474-1619a75d17aa',
    '__attentive_pv': '1',
    '__attentive_ss_referrer': 'https://www.chairish.com/collection/doors?q=doors&page=2',
    '_gid': 'GA1.2.393390075.1745494601',
    '__attentive_dv': '1',
    'sailthru_content': '18847a78b0c4eaaa50fa3ca09635173d',
    'sailthru_visitor': '9f3bc605-8b43-419d-b92e-004ca5464b01',
    'PLPopupClosed': '1',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Connection': 'keep-alive',
    'Referer': 'https://www.chairish.com/collection/doors?q=doors',
    # 'Cookie': 'csrftoken=l5IujLDZWrKb8gszAoef6slI3Q8K9Pia; guid=$d4c418c8-f118-4f2c-b28c-8843407b47e4; __utmz_chairish_02_11=1745396779.utmcsr=google|utmcmd=organic|utmccn=(organic)|utmctr=(not%20provided); amplitude_id_1d2656bc9b05970f4174110ee401a478chairish.com=eyJkZXZpY2VJZCI6ImNmYThlZjlhLTI5YjEtNGJmYy05YjBkLTgxZmRjNjgxNDk0OFIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTc0NTQ5NDU4NTExNSwibGFzdEV2ZW50VGltZSI6MTc0NTQ5NDYzMDI0MywiZXZlbnRJZCI6ODQsImlkZW50aWZ5SWQiOjI1LCJzZXF1ZW5jZU51bWJlciI6MTA5fQ==; _ga_2N8GB7SB99=GS1.1.1745494596.2.1.1745494598.0.0.0; _ga=GA1.2.1970461985.1745396780; _gcl_au=1.1.1892184413.1745396780; _attn_=eyJ1Ijoie1wiY29cIjoxNzQ1Mzk2Nzc5ODUyLFwidW9cIjoxNzQ1Mzk2Nzc5ODUyLFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcImFlODQ0YWRkY2FhNjQ2NzVhZDY1OWJkNGJkYTIwN2JjXCJ9Iiwic2VzIjoie1widmFsXCI6XCJhYzRiMjI2ZTBhZmM0MWNiYTBkNzJmYWMxOGZmOWUxMFwiLFwidW9cIjoxNzQ1NDk0NTk4MzE1LFwiY29cIjoxNzQ1NDk0NTk4MzE1LFwibWFcIjowLjAyMDgzMzMzMzMzMzMzMzMzMn0ifQ==; __attentive_id=ae844addcaa64675ad659bd4bda207bc; __attentive_cco=1745396779852; _pin_unauth=dWlkPU5URTFNVFF3TTJJdE56bGpOeTAwT0dNM0xUaGlPVFl0TkdSaVpUZG1OVEJsTkRKag; __utma=201483203.1970461985.1745396780.1745396781.1745494598.2; __utmc=201483203; __utmz=201483203.1745396781.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); tag_user_id=cec0c20e-a377-4215-833b-462d9910d64f-1745396779851; _fbp=fb.1.1745396781848.554942937678278344; _attn_bopd_=none; fct=0; MCEvilPopupClosed=1; __utmb=201483203.1.10.1745494598; __utmt=1; __attentive_session_id=ac4b226e0afc41cba0d72fac18ff9e10; _uetsid=62787560210011f0b954993f3d8d4ccb; _uetvid=a1f1da70201c11f095545d10590a6661; tag_session=5caf641b-4750-4013-8632-92e093dc1b30-2ea2830f-e975-4d67-b880-927673ae3ab6; sailthru_pageviews=1; __attentive_client_user_id=$0e5044e4-8b9e-47da-b474-1619a75d17aa; __attentive_pv=1; __attentive_ss_referrer=https://www.chairish.com/collection/doors?q=doors&page=2; _gid=GA1.2.393390075.1745494601; __attentive_dv=1; sailthru_content=18847a78b0c4eaaa50fa3ca09635173d; sailthru_visitor=9f3bc605-8b43-419d-b92e-004ca5464b01; PLPopupClosed=1',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=0, i',
}

params = {
    'q': 'doors',
    'page': '2',
}

response = requests.get('https://www.chairish.com/collection/doors', params=params, cookies=cookies, headers=headers)

js = BeautifulSoup(response.text,'html.parser')

script_tag = js.find('script',string= re.compile("context.PRODUCT_ID_TO_PRODUCT_JSON_MAP"))

if script_tag:
    script = re.search("context.PRODUCT_ID_TO_PRODUCT_JSON_MAP = ({.*?});",script_tag.string, re.DOTALL)
    json_data = json.loads(script.group(1))

    for key, value in json_data.items():
        prod_name =  value.get("title")
        id = value.get('id')
        pro_link = 'https://www.chairish.com' + value.get('url')

        price = value.get('your_price').get('current').get('value')
        display	 = value.get('your_price').get('current').get('display')
        verbose	 = value.get('your_price').get('current').get('verbose')

        dictionary = {"id": id,
                      "prod_name": prod_name,
                      "price": price,
                      "display": display,
                      "verbose": verbose,
                      "pro_link": pro_link} 
        print(dictionary)


