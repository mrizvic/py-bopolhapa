#!/bin/env python

import urllib
import urllib2
import json
import sys

from pyquery import PyQuery as pq
from lxml import etree
from collections import OrderedDict


class Bopolhapa(object):
	def __init__(self,search,sort=1):
		self.search=search
		self.sort=sort
		self.__Request(search,sort)

		buffer=self.__Request(search,sort)

		d=pq(buffer)
		ads=len(d('div.ad'))

		for j in xrange(ads):
			title=d('div.ad').find('div.coloumn.content').eq(j).find('a').text()
			href=d('div.ad').find('div.coloumn.content').eq(j).find('a').attr('href')
			content=d('div.ad').find('div.coloumn.content').eq(j).text()
			content=content.lstrip(title)
			img=d('div.ad').find('div.coloumn.image').eq(j).find('img').attr('data-original')
			price=d('div.ad').find('div.coloumn.prices').eq(j).find('div').text()

			values=OrderedDict([
								('id', j),
								('title', title),
								('content',content),
								('href',href),
								('img',img),
								('price',price)
								])

			sys.stdout.write(json.dumps(values, sort_keys=False))


	def __Request(self,search,sort=1,timeout=5):
		if search=="":
			raise ValueError('search string seems empty')
		if sort <> 1:
			raise ValueError('TODO: implement input validation')

		url='http://www.bopolhapa.com/iskanje'
		data={'q':search,'sort':sort}
		data=urllib.urlencode(data)
		
		try:
			request=urllib2.Request(url,data)
			response=urllib2.urlopen(request,timeout=timeout)
			buffer=response.read()
			return buffer
		except Exception as e:
			raise e



		
def main():
	b=Bopolhapa(search='commodore 64',sort=1)


if __name__ == '__main__':
	main()
