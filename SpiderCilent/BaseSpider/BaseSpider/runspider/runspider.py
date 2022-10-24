import sys
import os
from scrapy.cmdline import execute

from BaseSpider.settings import http

spider_id = int(sys.argv[1])

spider_model = http.request(r'spider_model_query', {'spider_id': spider_id}).json()['spider']
model_name = spider_model['model_name']
base_key = spider_model['base_key']

os.chdir('../runspider')
testcmd = 'python test.py {id} {base_key}'
testcmd = testcmd.format(id=spider_id, base_key=base_key)
os.system(testcmd)


os.chdir('../spiders')
spidercmd = "scrapy crawl BASE_SPIDER -a id=" + str(spider_id)

execute(spidercmd.split())


