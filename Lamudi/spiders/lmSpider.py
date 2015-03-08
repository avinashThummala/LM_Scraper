#!/usr/bin/python   
# -*- coding: utf-8 -*-

import scrapy, sys, traceback, os, time, urllib2
from level3 import *
from Lamudi.items import LamudiItem

from scrapy.http import Request
from scrapy import Selector
from scrapy import signals

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DOMAIN = 'lamudi.com.mx'
URL_PREFIX = 'http://'+DOMAIN
WAIT_TIME_FOR_ELEMENT = 6
SLEEP_TIME = 3
PAGE_LOAD_TIMEOUT = 180

dummyURL = 'http://www.lamudi.com.mx/tlalpan-a-una-calle-insurgentes-sur-atras-hospital-san-rafael-110167-16.html'

class LMSpider(scrapy.Spider):

    name = 'lmspider'
    allowed_domains = [DOMAIN]
    start_urls = getStartURLS()

    def initiateDriver(self):

        self.driver = webdriver.PhantomJS(service_args=['--load-images=no'])
        """
        options = webdriver.ChromeOptions()
        options.add_extension("Block-image_v1.0.crx")
        self.driver = webdriver.Chrome(chrome_options = options) 
        """

        self.driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        self.driver.maximize_window()

        self.enterEmailInfo()        

    def enterEmailInfo(self):

        try:
            self.loadUrl(dummyURL)

            WebDriverWait(self.driver, WAIT_TIME_FOR_ELEMENT).until(EC.presence_of_element_located((By.XPATH, "//a[@class=\'btn btn-primary phone-agent-button\']")) ).click()
            time.sleep(SLEEP_TIME)

            WebDriverWait(self.driver, WAIT_TIME_FOR_ELEMENT).until(EC.presence_of_element_located((By.ID, "RequestPhoneForm_email")) )
            self.driver.execute_script(' document.getElementById("RequestPhoneForm_email").value="dhthummala@gmail.com"; document.getElementById("RequestPhoneForm_acceptemailoffers").checked=true; ')
            WebDriverWait(self.driver, WAIT_TIME_FOR_ELEMENT).until(EC.presence_of_element_located((By.XPATH, "//form[@id=\'form-request-phone\']/fieldset/button")) ).click()        

        except:
            print traceback.format_exc()        

    def loadUrl(self, url):

        try:
            self.driver.get(url)

        except:

            print "*Get URL timed out*"
 
            if self.driver:
                self.driver.quit()

            self.initiateDriver()
            self.loadUrl(url)

    def __init__(self):
        self.initiateDriver()

    def getAgentTelephone(self, url, newItem):

        self.loadUrl(url)

        try:
            WebDriverWait(self.driver, WAIT_TIME_FOR_ELEMENT).until(EC.presence_of_element_located((By.XPATH, "//a[@class=\'btn btn-primary phone-agent-button\']")) ).click()
            time.sleep(SLEEP_TIME)

            oPhone = WebDriverWait(self.driver, WAIT_TIME_FOR_ELEMENT).until(EC.presence_of_element_located((By.XPATH, u"//table[@class=\'table-striped phone-link\']/tbody")) )            
            
            newItem['LM_Telefono_de_la_oficina'] = self.wdExtractText( u"//table[@class=\'table-striped phone-link\']/tbody/tr/td[text()=\'Tel\xe9fono de la oficina:\']/following-sibling::td")
            newItem['LM_Telefono_movil'] = self.wdExtractText( u"//table[@class=\'table-striped phone-link\']/tbody/tr/td[text()=\'Tel\xe9fono M\xf3vil:\']/following-sibling::td")
            newItem['LM_Telefono_adicional_de_contacto'] = self.wdExtractText( u"//table[@class=\'table-striped phone-link\']/tbody/tr/td[text()=\'Tel\xe9fono adicional de contacto:\']/following-sibling::td")

        except:
            print "Either the agent's phone numbers don't exist or was unable to load them even after "+str(WAIT_TIME_FOR_ELEMENT)+" seconds"
            print "URL -> "+url
            print traceback.format_exc()

            newItem['LM_Telefono_de_la_oficina'] = ''
            newItem['LM_Telefono_movil'] = ''
            newItem['LM_Telefono_adicional_de_contacto'] = ''

    def wdExtractText(self, xPathStr):

        try:
            return self.driver.find_element_by_xpath(xPathStr).text.strip()
        except:
            return ''

    def extractText(self, eList, index):

        if len(eList)>index:
            return eList[index].strip()
        else:
            return ''     

    def extractAdCode(self, hxs):

        for x in hxs.xpath("//div[@class=\'property-id\']/p/text()").extract():
            x=x.strip()
            if x:
                return x
        return ''

    def getListOfPhotos(self, hxs, newItem):

        vPicList= ['LM_Photo_1', 'LM_Photo_2', 'LM_Photo_3', 'LM_Photo_4', 'LM_Photo_5', 'LM_Photo_6', 'LM_Photo_7', 'LM_Photo_8',
                    'LM_Photo_9', 'LM_Photo_10']

        for x in vPicList:
            newItem[x] = ''

        index=0

        for x in hxs.xpath("//div[@class=\'carousel-inner\']/div/a/img/@data-original").extract():
        
            newItem[vPicList[index]] = x
            index=index+1

            if index>9:
                break

    def extractLocation(self, hxs, newItem):

        newItem['LM_Estado'] = ''
        newItem['LM_Municipio_o_Delegacion'] = ''
        newItem['LM_Colonia'] = ''        
        newItem['LM_Tipo_de_inmueble'] = ''        

        for string in hxs.xpath("//ul[@class=\'breadcrumb\']/li[position()>1]/a/@title").extract():

            if string.startswith('Estado: '):
                newItem['LM_Estado'] = string[8:].strip()

            elif string.startswith('Municipio: '):
                newItem['LM_Municipio_o_Delegacion'] = string[11:].strip()        

            elif string.startswith(u'\xc1rea: '):
                newItem['LM_Colonia'] = string[6:].strip()

            else:
                newItem['LM_Tipo_de_inmueble'] = string.strip()
                break

    def loadPrice(self, pValueStr, newItem):

        newItem['LM_Moneda'] = ''
        newItem['LM_Precio'] = ''

        if pValueStr.startswith('$'):
            newItem['LM_Moneda'] = u'MXN'

        elif pValueStr.startswith('US$'):
            newItem['LM_Moneda'] = u'USD'

        pList = pValueStr.split(' ')

        if len(pList)>1:            
            newItem['LM_Precio'] = pList[1].strip()
   
    def parse(self, response):

        listHxs = Selector(response)

        nextURL = 'http://lamudi.com.mx'+listHxs.xpath('//div[@class=\'pagination\']/ul/li[last()]/a/@href').extract()[0]
        shouldExit = False

        if response.url == nextURL:
            shouldExit = True

        for url in listHxs.xpath("//div[@id=\'listings\']/article/header/h4/a/@href").extract():

            url=URL_PREFIX+url

            listResponse = urllib2.urlopen( urllib2.Request(url) )
            hxs = Selector(text=listResponse.read())

            newItem = LamudiItem()    
            newItem['LM_Listing_URL'] = url

            newItem['LM_Superficie'] = self.extractText( hxs.xpath(u"//tr[td[@class=\'attribute-label\']/text()=\'Superficie (m\xb2):\']/td[@class=\'value\']/text()").extract(), 0)             
            newItem['LM_Recamaras'] = self.extractText( hxs.xpath(u"//tr[td[@class=\'attribute-label\']/text()=\'Rec\xe1maras:\']/td[@class=\'value\']/text()").extract(), 0)
            newItem['LM_Banos'] = self.extractText( hxs.xpath(u"//tr[td[@class=\'attribute-label\']/text()=\'Ba\xf1os:\']/td[@class=\'value\']/text()").extract(), 0)
            newItem['LM_Estacionamientos'] = self.extractText( hxs.xpath(u"//tr[td[@class=\'attribute-label\']/text()=\'Estacionamientos:\']/td[@class=\'value\']/text()").extract(), 0)
            newItem['LM_Amueblado'] = self.extractText( hxs.xpath(u"//tr[td[@class=\'attribute-label\']/text()=\'Amueblado:\']/td[@class=\'value\']/text()").extract(), 0)
            newItem['LM_Disponible_a_partir_de'] = self.extractText( hxs.xpath(u"//tr[td[@class=\'attribute-label\']/text()=\'Disponible a partir de:\']/td[@class=\'value\']/text()").extract(), 0)
            newItem['LM_Condiciones_de_precio'] = self.extractText( hxs.xpath(u"//tr[td[@class=\'attribute-label\']/text()=\'Condiciones de Precio:\']/td[@class=\'value\']/text()").extract(), 0)

            newItem['LM_Conservacion'] = self.extractText( hxs.xpath(u"//tr/td[@class=\'attribute-label\'and text()=\'Conservaci\xf3n\']/following-sibling::td/text()").extract(), 0)
            newItem['LM_Mantenimiento'] = self.extractText( hxs.xpath(u"//tr/td[@class=\'attribute-label\'and text()=\'Mantenimiento\']/following-sibling::td/text()").extract(), 0)

            newItem['LM_Construido_Ano'] = self.extractText( hxs.xpath(u"//tr/td[@class=\'attribute-label\'and text()=\'Construido (A\xf1o)\']/following-sibling::td/text()").extract(), 0)
            newItem['LM_Nivel'] = self.extractText( hxs.xpath(u"//tr/td[@class=\'attribute-label\'and text()=\'Nivel\']/following-sibling::td/text()").extract(), 0)
            newItem['LM_Plantas'] = self.extractText( hxs.xpath(u"//tr/td[@class=\'attribute-label\'and text()=\'Plantas en total\']/following-sibling::td/text()").extract(), 0)
            newItem['LM_Deposito_Aval'] = self.extractText( hxs.xpath(u"//tr/td[@class=\'attribute-label\'and text()=\'Dep\xf3sito / Aval\']/following-sibling::td/text()").extract(), 0)
            newItem['LM_Comision_del_agente'] = self.extractText( hxs.xpath(u"//tr/td[@class=\'attribute-label\'and text()=\'Comisi\xf3n del agente (si existe)\']/following-sibling::td/text()").extract(), 0)

            newItem['LM_Titulo'] = self.extractText( hxs.xpath("//header/h1/text()").extract(), 0)
            newItem['LM_Descripcion'] = self.extractText( hxs.xpath("string(//section[@class=\'listing-description\']/p)").extract(), 0)

            pValueStr = self.extractText( hxs.xpath("//span[@class=\'price-value\']/text()").extract(), 0)
            self.loadPrice(pValueStr, newItem)

            self.extractLocation(hxs, newItem)

            newItem['LM_Direccion'] = self.extractText( hxs.xpath("//section[@class=\'listing-address\']/p/span[2]/text()").extract(), 0)
            newItem['LM_Categoria'] = self.extractText( hxs.xpath("//span[@class=\'rent-interval\']/text()").extract(), 0)

            newItem['LM_Latitude'] = self.extractText( hxs.xpath("//div[@id=\'googlemap\']/div[@id=\'map_canvas\']/@data-lat").extract(), 0)
            newItem['LM_Longitude'] = self.extractText( hxs.xpath("//div[@id=\'googlemap\']/div[@id=\'map_canvas\']/@data-lng").extract(), 0)

            self.getListOfPhotos(hxs, newItem)

            newItem['LM_Ad_Code'] = self.extractAdCode(hxs)
            newItem['LM_Nombre'] = self.extractText( hxs.xpath("//p[@class=\'contact-name\']/strong/text()").extract(), 0)

            if newItem['LM_Nombre']:
                newItem['LM_Agente'] = 1
            else:
                newItem['LM_Agente'] = 0      

            self.getAgentTelephone(url, newItem)                

            yield newItem                        
        
        if not shouldExit:
            yield Request(nextURL, callback=self.parse)