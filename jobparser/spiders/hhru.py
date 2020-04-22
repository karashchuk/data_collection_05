# -*- coding: utf-8 -*-
import scrapy
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
	name = 'hhru'
	allowed_domains = ['hh.ru']
	#start_urls = ['https://hh.ru/search/vacancy?area=1&st=searchVacancy&text=Python&from=suggest_post']
	def __init__(self,searcher):
		self.start_urls = [f'https://hh.ru/search/vacancy?area=1&st=searchVacancy&text={searcher}&from=suggest_post']
	def parse(self, response):
		next_page = response.xpath("//a[@class='bloko-button HH-Pager-Controls-Next HH-Pager-Control']/@href").extract_first()
		
		if next_page:
			np = next_page[-2:]
			yield response.follow(next_page, callback=self.parse)
		else:
			np = 'finish'

		links = response.xpath("//a[contains(@data-qa,'vacancy-serp__vacancy-title')]/@href").extract()

		print(self.name, '----------page  ',np, '    записей   - ', len(links)) #оставил отметку чтобы видеть как идет процесс

		for link in links:
			yield response.follow(link, callback = self.vacancy_parse)
	def vacancy_parse(self, response):
		name_vac = response.xpath("//h1[@data-qa='vacancy-title']/text() | //h1[@data-qa='vacancy-title']/span/text()").extract_first()
		comp = response.xpath("//p[@class = 'vacancy-salary']/span[@data-qa='bloko-header-2']/text()").extract()
		empl = response.xpath("//a[contains(@data-qa, 'vacancy-company-name')]/span/text()").extract()
		url_link = response.url
		dom = self.allowed_domains[0]
		addr = response.xpath("//p[@data-qa='vacancy-view-location']/span[@data-qa='vacancy-view-raw-address']/text()").extract()
		#print(name_vac , comp)
		yield JobparserItem(name=name_vac, salary=comp, employer = empl, url = url_link, address = addr, site = dom)



