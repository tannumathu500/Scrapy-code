import scrapy
from bs4 import BeautifulSoup


class PhilippinesSpider(scrapy.Spider):
    name = "philippines"
    allowed_domains = ["yellow-pages.ph"]
    # start_urls = ["https://yellow-pages.ph"]

    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0"
               }
    
    def start_requests(self):
        url = 'https://www.yellow-pages.ph/category/wedding-and-bridal-shops/page-1'

        yield scrapy.Request(url, callback=self.first_page_data, headers=self.headers)

    def first_page_data(self, response):
        pro = response.xpath("//div[@class='search-listing']")
        for products in pro:
            pro_name = products.xpath(".//div[@class='search-business-name']//h2//a[@class='yp-click']//text()").get()
            pro_link = 'https://www.yellow-pages.ph' + products.xpath(".//div[@class='search-business-name']//h2//a[@class='yp-click']/@href").get()
            
            rating_from_5 = products.xpath(".//div[@class='search-rating-container']//div//div[@class='mr-1 text-muted']//text()").get()
            given_rating = products.xpath(".//div[@class='search-rating-container']//div//div[@class='search-star-number align-self-center ml-1']//text()").get()
            
            address = products.xpath(".//div[@class='search-busines-address']//span[@class='ellipsis']/text()").get()

            links = products.xpath(".//div[@class='d-flex']//a[contains(@class, 'btn') and contains(@class, 'yp-click')]/@href")
            map_media_link =  []
            tel_number = []

            for link in links:
                href = link.get() 
                if href.startswith("tel:"):
                    txt = href
                    tel_number.append(txt)
                else:
                    full_link = "https://www.yellow-pages.ph" + href
                    map_media_link.append(full_link)

            yield {"pro_name": pro_name,
                    "rating_from_5": rating_from_5,
                    "given_rating": given_rating,
                    "address": address,
                    "tel_number": ''.join(tel_number),
                    "full_link": map_media_link,
                    "pro_link": pro_link       
                }
        next = response.xpath("//a[@rel='next']/@href").get()
        if next:
            new_page = 'https://www.yellow-pages.ph' + next
            # print(new_page,'-------------------------------------------------------')

            yield scrapy.Request(new_page, callback=self.first_page_data, headers=self.headers)
