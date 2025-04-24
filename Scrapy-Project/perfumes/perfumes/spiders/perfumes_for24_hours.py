import scrapy
import scrapy.resolver
from bs4 import BeautifulSoup
import requests


class PerfumesFor24HoursSpider(scrapy.Spider):
    name = "perfumes_for24_hours"
    allowed_domains = ["perfume24x7.com"]
    # start_urls = ["https://perfume24x7.com"]

    def start_requests(self):

        url = 'https://www.perfume24x7.com/collections/women'
        # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0"}

        yield scrapy. Request(url, method='GET', callback=self.list_info)

    def list_info(self, main_url):
        soup = BeautifulSoup(main_url.text,'html.parser') 

        if soup.findAll('div','grid-product__content'):
            for product in soup.findAll('div','grid-product__content'):
                perfume_name = product.find('a','grid-product__link').find('div','grid-product__meta').find('div','grid-product__title grid-product__title--body').text
                perfume_link = 'https://www.perfume24x7.com/' + product.find('a','grid-product__link').get('href')

                yield {"perfume_name": perfume_name,
                       "perfume_link": perfume_link}
            
                yield scrapy.Request(perfume_link, method='GET', callback=self.detail_information, meta={"perfume_name":perfume_name, "perfume_link":perfume_link})

        next_page = soup.find('span', 'next')
        if next_page:
            page_urls = "https://www.perfume24x7.com" + next_page.find('a').get('href')
            print("next",'++++++++++++++++++++++',    page_urls, '=========================')

            yield scrapy.Request(page_urls,method='GET', callback=self.list_info )


    def detail_information(self, response):
        soup = BeautifulSoup(response.text,'html.parser')
        try:
            compared_price = soup.find('div','product-block product-block--price').find('span','product__price product__price--compare').text.replace('\n','')
        except:
            compared_price = ' '

        try:
            sale_price = soup.find('div','product-block product-block--price').find('span','product__price on-sale').text.replace('\n','')
        except:
            sale_price = ' '

        try:
            saving_price = soup.find('div','product-block product-block--price').find('span','product__price-savings').text.replace('\n','')
        except:
            saving_price = ' '

        try:
            reviews = soup.find('div','jdgm-prev-badge').text.strip()
        except:
            reviews = ' '

        small_desc = soup.find('div','product__policies rte small--text-center').text.replace('\n','')

        size = []
        try: 
            for k in soup.findAll('div','variant-input'):
                l = k.text
                size.append(l)
        except:
            l = ''

        sale_point = []
        try:
            for g in soup.findAll('div','product-block product-block--sales-point'):
                points = g.find('ul').find('li').find('span').find('span').text
                sale_point.append(points)
        except:
            points = ' '

        description = []
        try:
            for p in soup.find('div','collapsible-content__inner rte').findAll('p'):
                para = p.text.replace('\xa0','')
                description.append(para)       
        except:
            para = ''

        yield {"perfume_name": response.meta.get("perfume_name"),
               "perfume_link": response.meta.get("perfume_link"),
               "compared_price":compared_price,
               "sale_price": sale_price,
               "saving_price": saving_price,
               "reviews": reviews,
               "small_desc": small_desc,
               "sale_point": sale_point,
               "description": description}


    