#!/usr/bin/python   
# -*- coding: utf-8 -*-

import scrapy, sys
from Lamudi.items import LamudiItem

from scrapy.http import Request
from scrapy import Selector
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DOMAIN = 'lamudi.com.mx'
URL = 'http://lamudi.com.mx/todos'

dummyURL = 'http://www.lamudi.com.mx/habitaciones-en-renta-contrato-por-un-ao-a-5min-de-ave-constituyentes-252258-16.html?s_special=all&s_dir=desc&disable_previous=true'

class LMSpider(scrapy.Spider):

    name = 'lmspider'
    allowed_domains = [DOMAIN]
    start_urls = [
        URL
    ]

    def __init__(self):

        firefoxProfile = webdriver.FirefoxProfile()
        firefoxProfile.set_preference('permissions.default.stylesheet', 2)
        firefoxProfile.set_preference('permissions.default.image', 2)
        firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

        self.driver = webdriver.Firefox(firefox_profile=firefoxProfile)

        """
        If you have PhantomJS 2.0 installed, use this code. Otherwise stick with usage of a Firefox webdriver

        self.driver = webdriver.PhantomJS(service_args=['--load-images=no'])
        self.driver.set_window_size(1120, 550)
        """

        self.enterEmailInfo()

    def extractText(self, xPathStr):

        try:
            return self.driver.find_element_by_xpath(xPathStr).text.strip()     
        except:    
            return ''

    def extractDescription(self, xPathStr):

        desc = ''

        for x in self.driver.find_elements_by_xpath(xPathStr):
            desc += x.text+"\n"

        return desc            


    def extractAttribute(self, xPathStr, attrStr):

        try:
            return self.driver.find_element_by_xpath(xPathStr).get_attribute(attrStr)   
        except:    
            return ''            


    def getListOfPhotos(self, newItem):

        vPicList= ['LM_Photo_1', 'LM_Photo_2', 'LM_Photo_3', 'LM_Photo_4', 'LM_Photo_5', 'LM_Photo_6', 'LM_Photo_7', 'LM_Photo_8',
                    'LM_Photo_9', 'LM_Photo_10']

        for x in vPicList:
            newItem[x] = ''

        index=0

        for x in self.driver.find_elements_by_xpath("//div[@class=\'carousel-inner\']/div/a/img"):
        
            newItem[vPicList[index]] = x.get_attribute('data-original')
            index=index+1

            if index>9:
                break

    def enterEmailInfo(self): 

        self.driver.get(dummyURL) 
        self.driver.find_element_by_xpath("//a[@class=\'btn btn-primary phone-agent-button\']").click()

        try:
            emailTextField = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "RequestPhoneForm_email")) )
            emailTextField.send_keys('dhthummala@gmail.com')

            self.driver.find_element_by_id("RequestPhoneForm_acceptemailoffers").click()                        
            self.driver.find_element_by_xpath("//form[@id=\'form-request-phone\']/fieldset/button").click()

        except:
            """
                Need to try another dummy url.
                Have a couple of them in place
            """

    def extractLocation(self, newItem):

        newItem['LM_Estado'] = ''
        newItem['LM_Municipio_o_Delegacion'] = ''
        newItem['LM_Colonia'] = ''        
        newItem['LM_Tipo_de_inmueble'] = ''        

        for x in self.driver.find_elements_by_xpath("//ul[@class=\'breadcrumb\']/li[position()>1]/a"):

            string = x.get_attribute('title')

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

        hxs = Selector(response)

        nextURL = 'http://lamudi.com.mx/'+hxs.xpath('//div[@class=\'pagination\']/ul/li[last()]/a/@href').extract()[0]
        shouldExit = False

        if response.url == nextURL:
            shouldExit = True

        for url in response.xpath("//div[@id=\'listings\']/article/header/h4/a/@href").extract():

            if not url.startswith('http://'):
                url= DOMAIN + url    

            newItem = LamudiItem()    
            newItem['LM_Listing_URL'] = url

            self.driver.get(url)
            
            newItem['LM_Superficie'] = self.extractText(u"//tr[td[@class=\'attribute-label\']/text()=\'Superficie (m\xb2):\']/td[@class=\'value\']")             
            newItem['LM_Recamaras'] = self.extractText( u"//tr[td[@class=\'attribute-label\']/text()=\'Rec\xe1maras:\']/td[@class=\'value\']" )
            newItem['LM_Banos'] = self.extractText( u"//tr[td[@class=\'attribute-label\']/text()=\'Ba\xf1os:\']/td[@class=\'value\']" )
            newItem['LM_Estacionamientos'] = self.extractText( u"//tr[td[@class=\'attribute-label\']/text()=\'Estacionamientos:\']/td[@class=\'value\']" )    
            newItem['LM_Amueblado'] = self.extractText( u"//tr[td[@class=\'attribute-label\']/text()=\'Amueblado:\']/td[@class=\'value\']" )        
            newItem['LM_Disponible_a_partir_de'] = self.extractText( u"//tr[td[@class=\'attribute-label\']/text()=\'Disponible a partir de:\']/td[@class=\'value\']" )        
            newItem['LM_Condiciones_de_precio'] = self.extractText( u"//tr[td[@class=\'attribute-label\']/text()=\'Condiciones de Precio:\']/td[@class=\'value\']" )        

            newItem['LM_Conservacion'] = self.extractText( u"//tr/td[@class=\'attribute-label\'and text()=\'Conservaci\xf3n\']/following-sibling::td" )                
            newItem['LM_Mantenimiento'] = self.extractText( u"//tr/td[@class=\'attribute-label\'and text()=\'Mantenimiento\']/following-sibling::td" )

            newItem['LM_Construido_Ano'] = self.extractText( u"//tr/td[@class=\'attribute-label\'and text()=\'Construido (A\xf1o)\']/following-sibling::td")
            newItem['LM_Nivel'] = self.extractText( u"//tr/td[@class=\'attribute-label\'and text()=\'Nivel\']/following-sibling::td")
            newItem['LM_Plantas'] = self.extractText( u"//tr/td[@class=\'attribute-label\'and text()=\'Plantas en total\']/following-sibling::td")
            newItem['LM_Deposito_Aval'] = self.extractText( u"//tr/td[@class=\'attribute-label\'and text()=\'Dep\xf3sito / Aval\']/following-sibling::td")
            newItem['LM_Comision_del_agente'] = self.extractText( u"//tr/td[@class=\'attribute-label\'and text()=\'Comisi\xf3n del agente (si existe)\']/following-sibling::td")

            newItem['LM_Titulo'] = self.extractText( "//header/h1")
            newItem['LM_Descripcion'] = self.extractDescription( "//section[@class=\'listing-description\']/p")

            pValueStr = self.extractText("//span[@class=\'price-value\']")

            self.loadPrice(pValueStr, newItem)
            self.extractLocation(newItem)

            newItem['LM_Direccion'] = self.extractText( "//section[@class=\'listing-address\']/p/span[2]")
            newItem['LM_Categoria'] = self.extractText( "//span[@class=\'rent-interval\']")                                                            

            newItem['LM_Latitude'] = self.extractAttribute( "//div[@id=\'googlemap\']/div[@id=\'map_canvas\']", "data-lat")
            newItem['LM_Longitude'] = self.extractAttribute( "//div[@id=\'googlemap\']/div[@id=\'map_canvas\']", "data-lng")
                        
            self.getListOfPhotos(newItem)

            newItem['LM_Nombre'] = self.extractText( "//p[@class=\'contact-name\']/strong")

            """
            Can be improved
            """

            if newItem['LM_Nombre']:
                newItem['LM_Agente'] = 1
            else:
                newItem['LM_Agente'] = 0      

            self.driver.find_element_by_xpath("//a[@class=\'btn btn-primary phone-agent-button\']").click()

            try:
                oPhone = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, u"//table[@class=\'table-striped phone-link\']/tbody")) )            
                
                newItem['LM_Telefono_de_la_oficina'] = self.extractText( u"//table[@class=\'table-striped phone-link\']/tbody/tr/td[text()=\'Tel\xe9fono de la oficina:\']/following-sibling::td")
                newItem['LM_Telefono_movil'] = self.extractText( u"//table[@class=\'table-striped phone-link\']/tbody/tr/td[text()=\'Tel\xe9fono M\xf3vil:\']/following-sibling::td")
                newItem['LM_Telefono_adicional_de_contacto'] = self.extractText( u"//table[@class=\'table-striped phone-link\']/tbody/tr/td[text()=\'Tel\xe9fono adicional de contacto:\']/following-sibling::td")

            except:

                newItem['LM_Telefono_de_la_oficina'] = ''
                newItem['LM_Telefono_movil'] = ''
                newItem['LM_Telefono_adicional_de_contacto'] = ''

            yield newItem
        
        if not shouldExit:                
            yield Request(nextURL, callback=self.parse)            
                                  