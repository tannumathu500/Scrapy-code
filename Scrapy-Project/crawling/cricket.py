import requests
from bs4 import BeautifulSoup as bs
import json
import pandas as pd

cookies = {
    '_gcl_au': '1.1.1406136287.1745316090',
    '_ga_ESYQQV29YS': 'GS1.1.1745316090.1.1.1745316790.59.0.0',
    '_ga': 'GA1.2.743781741.1745316090',
    'form_key': 'g5olsa7YMrA9cigA',
    'mage-cache-storage': '{}',
    'mage-cache-storage-section-invalidation': '{}',
    'mage-cache-sessid': 'true',
    'mage-messages': '',
    'recently_viewed_product': '{}',
    'recently_viewed_product_previous': '{}',
    'recently_compared_product': '{}',
    'recently_compared_product_previous': '{}',
    'product_data_storage': '{}',
    '_fbp': 'fb.1.1745316093394.369245280780592728',
    '_gid': 'GA1.2.573971768.1745316094',
    '_gat': '1',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://www.dsc-cricket.com/gear/cricket-bats.html?srsltid=AfmBOopwBr5K_uxIyvr7U_ciYOYgtKtgI4tJaNMMq9HjbGVVOEL2Mc1F',
    'Connection': 'keep-alive',
    # 'Cookie': '_gcl_au=1.1.1406136287.1745316090; _ga_ESYQQV29YS=GS1.1.1745316090.1.1.1745316790.59.0.0; _ga=GA1.2.743781741.1745316090; form_key=g5olsa7YMrA9cigA; mage-cache-storage={}; mage-cache-storage-section-invalidation={}; mage-cache-sessid=true; mage-messages=; recently_viewed_product={}; recently_viewed_product_previous={}; recently_compared_product={}; recently_compared_product_previous={}; product_data_storage={}; _fbp=fb.1.1745316093394.369245280780592728; _gid=GA1.2.573971768.1745316094; _gat=1',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=0, i',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

break_url = headers['Referer'].split('?')[0].replace('gear/cricket-bats.html','')
end_url = headers['Referer'].split('?')[0].replace('https://www.dsc-cricket.com/','')

url = break_url+end_url
# print(url)

while url:
    response = requests.get(url, cookies=cookies, headers=headers)
    print(response,'       ', url)
    js = bs(response.text,'html.parser')
    for pro in js.findAll('div','product-item-info'):
        name = pro.find('h4','product name product-item-name').find('a').text.strip()
        links = name = pro.find('h4','product name product-item-name').find('a').get('href')
        print(links)


    next_url = js.find('li','item pages-item-next')
    if next_url:
        next = next_url.find('a','action next').get('href')
        url = next
        print('-----------------------',url,'--------------------------')
    else:
        break

# Want to extract only certain fields from each item (like price, image, etc.)?