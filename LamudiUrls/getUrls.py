#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy, urllib2
from scrapy import Selector

addURL="http://www.lamudi.com.mx"

pURL1="http://www.lamudi.com.mx/todos"
pURL2=[]
pURL3=[]
pURL4=[]

def parseRegions(data):

	global pURL2
	hxs = Selector(text=data)

	for x in hxs.xpath("//div[@id=\'location_region\']/div[@class=\'facet-values\']/a/@href").extract():
		pURL2.append(addURL+x)

def parseCities(data):

	global pURL3
	hxs = Selector(text=data)

	for x in hxs.xpath("//div[@id=\'location_city\']/div[@class=\'facet-values\']/a/@href").extract():
		pURL3.append(addURL+x)		

def parseAreas(data):

	global pURL4
	hxs = Selector(text=data)

	for x in hxs.xpath("//div[@id=\'location_area\']/div[@class=\'facet-values\']/a/@href").extract():
		pURL4.append(addURL+x)

response = urllib2.urlopen(urllib2.Request(pURL1))
parseRegions(response.read())		

for x in pURL2:
	response = urllib2.urlopen(urllib2.Request(x))
	parseCities(response.read())

for x in pURL3:
	response = urllib2.urlopen(urllib2.Request(x))
	parseAreas(response.read())	

print pURL4