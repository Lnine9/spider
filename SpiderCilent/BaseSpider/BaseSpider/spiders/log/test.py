from queue import Queue

from BaseSpider.data_operate.spider_manage.crawl_html import CrawlHtml

data_queue = Queue(maxsize=0)

def get_data_id_queue():
    data_list = CrawlHtml.query_BySpiderID(1)
    for item in data_list:
        data_queue.put(item.id)
    cdl_size = data_queue.qsize()
    print(cdl_size)

get_data_id_queue()