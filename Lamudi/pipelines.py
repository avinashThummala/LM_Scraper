# -*- coding: utf-8 -*-

import sys
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request

class LamudiPipeline(object):

	def __init__(self):

		self.conn = MySQLdb.connect(user='root', passwd='baggio', db='pyScrapper', host='localhost', charset="utf8", use_unicode=True)
		self.cursor = self.conn.cursor()

	def getInteger(self, intStr):

		intStr = re.sub("[^0123456789-]", '', intStr)

		if intStr:
			return int(intStr)		
		else:
			return None		

	def getCoordinate(self, floatStr):

		floatStr = re.sub("[^0123456789\.-]", '', floatStr)

		if floatStr:
			return float(floatStr)		
		else:
			return None							

	def getFloat(self, floatStr):

		floatStr = re.sub("[^0123456789\.]", '', floatStr)

		if floatStr:
			return float(floatStr)		
		else:
			return None			

	def process_item(self, item, spider): 

		if newItem['LM_Amueblado']:
			newItem['LM_Amueblado']=1
		else:						
			newItem['LM_Amueblado']=0														

		try:

			self.cursor.execute("""INSERT INTO lamudi VALUES (

				%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
				%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s 
				        	
				)""", (

					newItem['LM_Listing_URL'].encode('utf-8'),

					newItem['LM_Agente'],
					newItem['LM_Tipo_de_inmueble'].encode('utf-8'),

					self.getFloat(newItem['LM_Superficie']),
					self.getInteger(newItem['LM_Recamaras']),
					self.getFloat(newItem['LM_Banos']),
					self.getInteger(newItem['LM_Nivel']),

					self.getInteger(newItem['LM_Plantas']),
					newItem['LM_Disponible_a_partir_de'].encode('utf-8'),
					newItem['LM_Conservacion'].encode('utf-8'),

					newItem['LM_Titulo'].encode('utf-8'),
					newItem['LM_Descripcion'].encode('utf-8'),

					self.getFloat(newItem['LM_Precio']),
					newItem['LM_Moneda'].encode('utf-8'),

					newItem['LM_Estado'].encode('utf-8'),
					newItem['LM_Municipio_o_Delegacion'].encode('utf-8'),
					newItem['LM_Colonia'].encode('utf-8'),
					
					newItem['LM_Nombre'].encode('utf-8'),
					newItem['LM_Telefono_de_la_oficina'].encode('utf-8'),
					newItem['LM_Telefono_movil'].encode('utf-8'),
					newItem['LM_Telefono_adicional_de_contacto'].encode('utf-8'),

					self.getInteger(newItem['LM_Construido_Ano']),
					self.getInteger(newItem['LM_Estacionamientos']),

					newItem['LM_Amueblado'],
					newItem['LM_Categoria'].encode('utf-8'),
					newItem['LM_Direccion'].encode('utf-8'),

					self.getCoordinate(newItem['LM_Latitude']),				
					self.getCoordinate(newItem['LM_Latitude']),											

					newItem['LM_Condiciones_de_precio'].encode('utf-8'),
					newItem['LM_Deposito_Aval'].encode('utf-8'),
					self.getFloat(newItem['LM_Mantenimiento']),
					self.getFloat(newItem['LM_Comision_del_agente']),

					newItem['LM_Photo_1'].encode('utf-8'),
					newItem['LM_Photo_2'].encode('utf-8'),
					newItem['LM_Photo_3'].encode('utf-8'),
					newItem['LM_Photo_4'].encode('utf-8'),
					newItem['LM_Photo_5'].encode('utf-8'),
					newItem['LM_Photo_6'].encode('utf-8'),
					newItem['LM_Photo_7'].encode('utf-8'),
					newItem['LM_Photo_8'].encode('utf-8'),
					newItem['LM_Photo_9'].encode('utf-8'),
					newItem['LM_Photo_10'].encode('utf-8')
			))

			self.conn.commit()

			return item

		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])	       
			return item
