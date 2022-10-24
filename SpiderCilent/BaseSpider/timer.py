import os

from apscheduler.schedulers.blocking import BlockingScheduler
from BaseSpider.data_operate.spider_manage import spider_model

def job(spiderid):
    os.chdir('./BaseSpider/runspider')
    testcmd = 'runspider.py {spiderid}'
    testcmd = testcmd.format(spiderid=spiderid)
    os.system(testcmd)

if __name__ == '__main__':

    model = spider_model.queryid() # 获得需要爬虫的模块id

    scheduler = BlockingScheduler()
    # for item in model:
    #     spider_id = item.id
    scheduler.add_job(job(7), 'interval', seconds=60)
    scheduler.start()