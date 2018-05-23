import scrapy


class SellCarSpider(scrapy.Spider):
    name = "sell_car_spider"
    allowed_domains = ["renrenche.com"]
    start_urls = [
        "https://www.renrenche.com/nj/ershouche/",
    ]
    city_url_template = "https://www.renrenche.com{city_url}ershouche/"

    def parse(self, response):
        city_span = response.xpath("//a[@class='province-item ']")
        for city in city_span:
            city_url = city.xpath("@href").extract()[0]
            city_name = city.xpath("text()").extract()[0]
            print(city_name, city_url)
            yield scrapy.Request(url=self.city_url_template.format(city_url=city_url), callback=self.parse_city)

    def parse_city(self, response):
        items_urls = response.xpath('//a[@rrc-event-param="search"]/@href').extract()
        for items_url in items_urls:
            yield scrapy.Request(url=response.urljoin(items_url), callback=self.parse_item)
        next_url = response.xpath('//a[@rrc-event-name="switchright"]/@href').extract()[0]
        yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse)

    def parse_item(self, response):
        title_name = response.xpath('//h1[contains(@class, "title-name")]/text()').extract()[0]
        car_city = response.xpath('//strong[@id="car-licensed"]/@licensed-city').extract()[0]
        print(title_name, car_city)
