# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from pprint import pprint
import re

class JobparserPipeline(object):
	def __init__(self):
		client = MongoClient('localhost',27017)
		self.db = client.job 

	def process_item(self, item, spider):
		collection = self.db[spider.name]
		comp = item['salary']
		if spider.name =='hhru':
			if 'от ' in comp:
				sal_min=int((comp[comp.index('от ')+1]).replace('\xa0',''))
			else:
				sal_min=None
			if ' до ' in comp:
				sal_max=int((comp[comp.index(' до ')+1]).replace('\xa0',''))
			else:
				sal_max=None
			if (sal_min or sal_max): 
				if len(comp[-1]) > 5:
					curency = comp[-2]
				else:
					curency = comp[-1]
			else:
				curency = None
			empl = ''.join(item['employer'])
			addr = item['address']
			addr2 = [i for i in addr if i !=', ']
			addr1 = ''.join(addr2)
		else:
			empl = item['employer']
			addr1 = item['address']
			if 'до' in comp:
				sal=((comp[2]).replace('\xa0',''))
				sal_max = int(re.findall(r'\d+',sal)[0])
				sal_min = None
				curency = re.findall(r'[a-zA-Zа-яА-Я]+',(re.findall(r'\d+[a-zA-Zа-яА-Я]+',sal)[0]))[0]
			elif 'от' in comp:
				sal=((comp[2]).replace('\xa0',''))
				sal_min = int(re.findall(r'\d+',sal)[0])
				sal_max = None
				curency = re.findall(r'[a-zA-Zа-яА-Я]+',(re.findall(r'\d+[a-zA-Zа-яА-Я]+',sal)[0]))[0]
			elif comp[-1] == 'руб.':
				sal_min=int((comp[0]).replace('\xa0',''))
				sal_max=int((comp[1]).replace('\xa0',''))
				curency = comp[-1]
			else:
				sal_min = None
				sal_max = None
				curency = None
		collection.insert_one({'name':item['name'], 'sal_min':sal_min, 'sal_max': sal_max, 'curency':curency,'employer': empl, 'url': item['url'], 'address': addr1 , 'site': item['site'] } )
		return item
