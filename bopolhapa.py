#!/bin/env python

import urllib
import urllib2
import json

from pyquery import PyQuery as pq
from lxml import etree
from collections import OrderedDict


class Bopolhapa(object):
	def __init__(self):
		return None

	def query(self,search,sort=1):
		buffer=self.__Request(search,sort)

		# file='bopolhapa'
		# with open(file) as f:
		# 	buffer=f.read()

		buffer=buffer.translate(None, '\t\n')
		d=pq(buffer)

		ads=len(d('div.ad'))

		self.items=[]

		for i in xrange(ads):
			title=d('div.ad').find('div.coloumn.content').eq(i).find('a').text()
			href=d('div.ad').find('div.coloumn.content').eq(i).find('a').attr('href')
			content=d('div.ad').find('div.coloumn.content').eq(i).text()
			content=content[len(title)+1:]
			img=d('div.ad').find('div.coloumn.image').eq(i).find('img').attr('data-original')
			price=d('div.ad').find('div.coloumn.prices').eq(i).find('div').text()

			values=OrderedDict([
								('item', i),
								('title', title),
								('content',content),
								('href',href),
								('img',img),
								('price',price)
								])
			self.items.append(values)
		return self.items

	def jsonize(self,items):
		jsonitems={'results': items}
		return json.dumps(jsonitems)


	def __Request(self,search,sort=1,timeout=5):
		if search=="":
			raise ValueError('search string seems empty')
		if sort < 1 or sort > 4:
			#1 - zadnji vpisani oglasi naprej
			#2 - oglasi pred potekom naprej
			#3 - oglasi z nizjo ceno naprej
			#4 - oglasi z visjo ceno naprej
			raise ValueError('sort should be in range(1,4)')

		url='http://www.bopolhapa.com/iskanje'
		data={'q':search,'sort':sort}
		data=urllib.urlencode(data)
		
		try:
			headers = { 'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)' }
			request=urllib2.Request(url,data,headers)
			response=urllib2.urlopen(request,timeout=timeout)
			buffer=response.read()
			return buffer
		except Exception as e:
			raise e


		
def main():
	b=Bopolhapa()
	result=b.query(search='raspberry pi')
	json=b.jsonize(result)
	print json

if __name__ == '__main__':
	main()
