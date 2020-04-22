# -*- coding: utf-8 -*-
import scrapy
from jobparser.items import JobparserItem

class SjobruSpider(scrapy.Spider):
	name = 'sjobru'
	allowed_domains = ['superjob.ru']

	def __init__(self,searcher):
		self.start_urls = [f'https://www.superjob.ru/vacancy/search/?keywords={searcher}&geo%5Bc%5D%5B0%5D=1']
	def parse(self, response):
		next_page = response.xpath("//a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']/@href").extract_first()
		
		if next_page:
			np = next_page[-2:]
			yield response.follow(next_page, callback=self.parse)
		else:
			np = 'finish'

		links = response.xpath("//div[@class='QiY08 LvoDO']//div[contains(@class,'_3mfro CuJz5 PlM3e _2JVkc _3LJqf')]/a/@href").extract()

		print(self.name,'----------page  ',np, '    записей   - ', len(links)) #оставил отметку чтобы видеть как идет процесс

		for link in links:
			yield response.follow(link, callback = self.vacancy_parse)
	def vacancy_parse(self, response):
		name_vac = response.xpath("//h1[@class='_3mfro rFbjy s1nFK _2JVkc']/text()").extract_first()
		comp = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/text()").extract()
		empl = response.xpath("//div[@class='_1Tjoc _3ifBO Ghoh2 _3lvIR']//div[@class='_1cFsi _3VUIu']/div[@class='_2g1F-'][1]//h2/text()").extract_first()
		url_link = response.url
		dom = self.allowed_domains[0]
		addr = response.xpath("//div[@class='f-test-address _3AQrx']//span[@class='_3mfro _1hP6a _2JVkc']/text()").extract_first()
		#print(name_vac , comp)
		yield JobparserItem(name=name_vac, salary=comp, employer = empl, url = url_link, address = addr, site = dom)