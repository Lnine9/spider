from django.http import JsonResponse, HttpResponse


from .config import http_code
from .server.task import running
from .service import spiderService, m_scrapyd, spider_scheduler

running()

'''
启动爬虫
'''


def launching(request):
    # 检查 爬虫 状态，如果有正在运行的 job，则返回 '爬虫无法重复启动'
    # 不执行后续逻辑
    spider_id = request.GET.get("spider_id")
    job_id = spiderService.check_spider_status(spider_id)
    result = spiderService.launching(spider_id)
    return JsonResponse({'status': http_code.SUCCESS, 'message': result, 'spiders': spider_id})
    # return JsonResponse({'status': http_code.EXCPTION, 'message': '爬虫无法重复启动', 'spiders': spiders})


'''
查看 爬虫 的状态
'''


def sp_status(request):
    spider_id = request.GET.get("spider_id")
    spiders = reset_all_status()
    job_id = spiderService.check_spider_status(spider_id)
    if job_id is not '' and job_id is not None:
        m_status = 'running'
    else:
        m_status = 'finished'
    return JsonResponse({'status': '200', 'message': m_status, 'spiders': spiders})


'''
停止爬虫
'''


def stop_spider(request):
    # 检查爬虫状态
    # 如果未运行，则返回 '该爬虫未启动'，不执行之后逻辑
    spider_id = request.GET.get("spider_id")
    spiders = reset_all_status()
    job_id = spiderService.check_spider_status(spider_id)
    # 判定是否真实运行
    if job_id is not '' and job_id is not None:
        spiderService.stop_spider('BASE_SPIDER', job_id)
        spiderService.update_job_status(job_id, 'finished')
        spiders = reset_all_status()
        return JsonResponse({'status': '200', 'message': '爬虫已停止', 'spiders': spiders})
    return JsonResponse({'status': '300', 'message': '该爬虫未启动', 'spiders': spiders})


'''
查看所有爬虫状态
'''


def all_spiders(request):
    spiders = reset_all_status()
    lists = m_scrapyd.list_jobs(project="BASE_SPIDER")['running']
    if lists:
        min = lists[0]
        for l in lists[1:]:
            if l['start_time'] < min['start_time']:
                min = l
    else:
        min = {}
    return JsonResponse({'status': '200', 'spiders': spiders, 'oldSpider': min})


'''
重设所有状态
'''


def reset_all_status():
    # 在进程中查询所有正在运行的 job
    # 对应正在运行的 job 所属爬虫，设置爬虫状态
    spiderService.query_running_sid()
    spiders = spiderService.reset_all_status()

    return spiders


"""
向调度队列中添加爬虫
"""


def scheduler_add(request):
    spider_id = request.GET.get("spider_id")
    info = spider_scheduler.add_spider(spider_id)
    return JsonResponse({'status': '200', 'data': info})


"""
从调度队列中移除爬虫
"""


def scheduler_remove(request):
    spider_id = request.GET.get("spider_id")
    info = spider_scheduler.remove_spider(spider_id)
    return JsonResponse({'status': '200', 'data': info})


"""
启用调度
"""


def scheduler_start(request):
    info = spider_scheduler.begin_scheduler()
    return JsonResponse({'status': '200', 'data': info})


"""
停止调度
"""


def scheduler_shutdown(request):
    info = spider_scheduler.close_scheduler()
    return JsonResponse({'status': '200', 'data': info})


"""
调度列表
"""


def scheduler_list(request):
    return JsonResponse(spider_scheduler.get_list())


def scheduler_log(request):
    return HttpResponse(spider_scheduler.read_log())
