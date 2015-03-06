# -*- coding: utf-8 -*-

# Scrapy settings for Lamudi project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'Lamudi'
DOWNLOAD_TIMEOUT = 30
CONCURRENT_REQUESTS = 3
DOWNLOAD_DELAY = 0.4

SPIDER_MODULES = ['Lamudi.spiders']
NEWSPIDER_MODULE = 'Lamudi.spiders'

ITEM_PIPELINES = {

    'Lamudi.pipelines.LamudiPipeline': 300,
}