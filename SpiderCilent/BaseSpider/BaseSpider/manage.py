#!/usr/bin/python
from scrapy.cmdline import execute
execute('scrapy crawl BASE_SPIDER  -s JOBDIR=log/ajlog'.split())