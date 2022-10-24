from apscheduler.schedulers.background import BackgroundScheduler

from SpiderClient.service import spiderService, spider_scheduler, spider_jobs
from SpiderClient.settings import http
from ..service import m_scrapyd

data = 'first_group'

spider_scheduler.begin_scheduler()


def get_running_spider():
    """
    所有正在运行的爬虫id
    :return:
    """
    run = []
    # 轮询队列中分段爬虫id
    pending_spider = [i.get('spider_id') for i in spider_scheduler.get_list().get('spider')]
    # scrapyd pending、running的爬虫id
    for pid in spider_scheduler.get_running_spider():
        for item in spider_jobs.items():
            key, value = item[0], item[1].job_id
            if value == pid:
                run.append(key)
    run += pending_spider
    run = list(set(run))
    return run



flag = True


def scheduler_task():
    global flag
    spider_list = get_running_spider()
    print('queue spider： ', spider_list)
    if not spider_list and flag:
        flag = False
        mission_spiders = http.session.get(url=r'http://39.100.86.12:8899/distributed/get/?password=' + data).json()
        zgzf = mission_spiders['ZGZF']
        print('mission_spiders： ', zgzf)
        spiderService.launching(zgzf.pop(0))
    if not spider_list and not flag:
        flag = True
    print(spider_list)



def running():
    bg_scheduler = BackgroundScheduler()
    bg_scheduler.add_job(scheduler_task, trigger='interval', minutes=5)
    bg_scheduler.start()
