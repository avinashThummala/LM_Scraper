# -*- coding: utf-8 -*-
import scrapy


class LamudiItem(scrapy.Item):

	LM_Listing_URL = scrapy.Field()
	LM_Ad_Code = scrapy.Field()

	LM_Agente = scrapy.Field()
	LM_Tipo_de_inmueble = scrapy.Field()

	LM_Superficie = scrapy.Field()
	LM_Recamaras = scrapy.Field()
	LM_Banos = scrapy.Field()

	LM_Nivel = scrapy.Field()
	LM_Plantas = scrapy.Field()
	LM_Disponible_a_partir_de = scrapy.Field()
	LM_Conservacion = scrapy.Field()

	LM_Titulo = scrapy.Field()
	LM_Descripcion = scrapy.Field()

	LM_Precio = scrapy.Field()
	LM_Moneda = scrapy.Field()

	LM_Estado = scrapy.Field()
	LM_Municipio_o_Delegacion = scrapy.Field()
	LM_Colonia = scrapy.Field()

	LM_Nombre = scrapy.Field()
	LM_Telefono_de_la_oficina = scrapy.Field()
	LM_Telefono_movil = scrapy.Field()
	LM_Telefono_adicional_de_contacto = scrapy.Field()

	LM_Construido_Ano = scrapy.Field()
	LM_Estacionamientos = scrapy.Field()
	LM_Amueblado = scrapy.Field()

	LM_Categoria = scrapy.Field()
	LM_Direccion = scrapy.Field()

	LM_Latitude = scrapy.Field()
	LM_Longitude = scrapy.Field()	

	LM_Condiciones_de_precio = scrapy.Field()
	LM_Deposito_Aval = scrapy.Field()
	LM_Mantenimiento = scrapy.Field()
	LM_Comision_del_agente = scrapy.Field()

	LM_Photo_1 = scrapy.Field()
	LM_Photo_2 = scrapy.Field()
	LM_Photo_3 = scrapy.Field()
	LM_Photo_4 = scrapy.Field()
	LM_Photo_5 = scrapy.Field()
	LM_Photo_6 = scrapy.Field()
	LM_Photo_7 = scrapy.Field()
	LM_Photo_8 = scrapy.Field()
	LM_Photo_9 = scrapy.Field()
	LM_Photo_10 = scrapy.Field()