from apscheduler.schedulers.background import BackgroundScheduler
from SpiderClient.service import m_scrapyd
from SpiderClient.service.pending_list import SchedulerInfo, PendingList, CrawlerTaskUnit, SpiderInfo
from SpiderClient.settings import http


def get_running_spider():
    """
    scrapyd中爬虫id
    :return:
    """
    scheduler_info = SchedulerInfo()
    try:
        jobs = m_scrapyd.list_jobs(scheduler_info.project_name)
        runnings = jobs['running'] + jobs['pending']
        running_ids = [ones['id'] for ones in runnings]
        return running_ids
    except:
        return []


def add_spider(spider_id):
    """
    爬虫加入队列
    :param spider_id:
    :return:
    """
    pending_list = PendingList()
    try:
        number = int(spider_id)
    except:
        info = "错误信息:" + str(spider_id)
        return info

    crawler_task_unit = pending_list.all_task.get(str(number), None)
    if crawler_task_unit is not None:
        pending_list.mission_accomplished(crawler_task_unit)
        info = {'id': spider_id, 'info': "爬虫状态更新"}
        return info
    else:
        spider = http.request(r'spider_list_query', {'spider_id': spider_id}).json()['spider']
        spider_info = SpiderInfo(spider_id=spider['id'])
        crawler_task_unit = CrawlerTaskUnit()
        crawler_task_unit.spider_info = spider_info
        crawler_task_unit.has_next = True
        pending_list.add_task(crawler_task_unit)
        info = {'id': spider_id, 'info': "加入爬虫"}
        return info


def timed_task():
    scheduler_info = SchedulerInfo()
    pending_list = PendingList()
    # 运行中爬虫
    runnings = get_running_spider()
    # 获得新增任务量
    need_number = scheduler_info.max_spider_number - len(runnings)
    # 更新就绪爬虫
    pending_list.reload_task()
    print("reload")
    if need_number > 0:
        # 获得就绪爬虫列表
        readys = pending_list.get_task(need_number)
        print("ready", readys)
        # 启动爬虫
        for si in readys:
            si.run_spider()


def begin_scheduler():
    scheduler_info = SchedulerInfo()
    if scheduler_info.bg_scheduler is None:
        scheduler_info.bg_scheduler = BackgroundScheduler()
    if scheduler_info.bg_scheduler.state == 0:
        scheduler_info.bg_scheduler.add_job(timed_task, id='task', trigger='interval', seconds=10)
        scheduler_info.bg_scheduler.start()
    return "调度启动"


def close_scheduler():
    scheduler_info = SchedulerInfo()
    PendingList().clear()
    scheduler_info.bg_scheduler.remove_all_jobs(jobstore=None)
    scheduler_info.bg_scheduler.shutdown(wait=False)
    return "调度关闭,队列清空"


def remove_spider(spider_id):
    pending_list = PendingList()
    pending_list.delete_task(pending_list.all_task.get(str(spider_id), None))
    return {'spider_id': spider_id}


def get_list():
    pending_list = PendingList()
    scheduler_info = SchedulerInfo()
    return {"spider": [{'spider_id': key, 'spider_job_id': value.spider_job_id, 'has_next': value.has_next,
                        'spider_stop_time': value.spider_stop_time, 'status': value.status.name}
                       for key, value in pending_list.all_task.items()],
            "scheduler_status": scheduler_info.bg_scheduler.state if scheduler_info.bg_scheduler else 0,
            "isRun": scheduler_info.bg_scheduler.state if scheduler_info.bg_scheduler else None,
            '队列地址': id(pending_list.all_task)}
