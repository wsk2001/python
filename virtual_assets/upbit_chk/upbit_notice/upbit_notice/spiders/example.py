# example.py
import scrapy

class ExampleSpider(scrapy.Spider):
    name = 'example'

    def start_requests(self):
        urls = [
            'https://upbit.com/service_center/notice/'
        ]

        return [scrapy.Request(url=url, callback=self.parse) for url in urls]
        # 또는
        #for url in urls
        #    yield scrapy.Reqest(url=url, callback=self.parse

    def parse(self, response):
        url = response.url
        title = response.css('h1::text').get()
        print(f'URL is: {url}')
        print(f'Title is: {title}')