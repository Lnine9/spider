import logging
from ..service import m_scrapyd
from django.http import JsonResponse
from ..entity.spider_job import SpiderJob
from ..service import spider_jobs
from ..service import init_param
from ..settings import http

'''
加载配置启动爬虫
'''


def launching(m_id):
    # 加载配置启动爬虫
    # 如果数据库无对应爬虫，返回错误码
    # 将 job_id 记录内存，并设置状态
    spider = http.request(r'spider_list_query', {'spider_id': m_id}).json()['spider']

    if spider['id'] is None:
        return JsonResponse({'status': '300', 'message': '无法启动该爬虫'})

    spider_id = spider['id']

    # 其他爬虫
    if spider_id in ['2021']:
        m_scrapyd.schedule('FARM_MARKET_SPIDER', 'FARM_MARKET_SPIDER')

    else:
        # 向 redis 发送参数
        param = init_param.param_to_redis(m_id)
        logger = logging.getLogger('file_out.views')
        if not param['status']:
            logger.error(param['error'])
            return param['error']
        logger.error(param['redis-back'])

        m_job_id = m_scrapyd.schedule('BASE_SPIDER', 'BASE_SPIDER', id=spider_id)

        m_spider_job = SpiderJob(spider_id=spider_id, job_id=m_job_id, status='running')
        spider_jobs[spider_id] = m_spider_job

    return '爬虫启动成功'


'''
进程操作：检查 job 状态
'running'：正在运行
'pending'：准备运行
'finished'：完成运行
'''


def sp_status(project, job_id):
    job_status = m_scrapyd.job_status(project=project, job_id=job_id)
    return job_status


'''
进程操作：停止爬虫
清空redis
'''


def stop_spider(m_project, job_id):
    m_scrapyd.cancel(project=m_project, job=job_id, signal=None)
    return '爬虫已停止'


'''
进程操作：查询所有 job
'''


def all_spiders(project):
    m_spider_jobs = m_scrapyd.list_jobs(project=project)
    return m_spider_jobs


'''
内存操作：检查对应spider是否有对应正在运行的job
True: return job_id
False: return ''
'''


def check_spider_status(m_spider_id):
    if m_spider_id in spider_jobs.keys():
        return spider_jobs[m_spider_id].job_id
    return ''


'''
内存操作：更新 job 数据
'''


def update_job_status(m_job_id, m_status):
    for i in list(spider_jobs):
        if spider_jobs[i].job_id == m_job_id:
            spider_jobs[i].status = m_status


'''
数据库操作：获取爬虫列表
'''


def load_spider_list():
    query = {'operate': 'query', 'class_type': 'db.sm', 'class_name': 'SpiderList', 'query_info': {}}
    result = http.request(r'query', query).json()
    obj=object()
    obj.__dict__.update(result)
    return obj


'''
内存操作：获取 job 对应 爬虫id
'''


def load_sub_spider(m_job_id):
    for i in list(spider_jobs):
        if spider_jobs[i].job_id == m_job_id:
            return spider_jobs[i].spider_id
    return ''


'''
数据库操作：更新 job 对应 爬虫状态
'''


def upload_sub_spider(m_spider_id, m_status):
    update = {'operate': 'deal',
              'items': {'class_type': 'db.sm', 'class_name': 'SpiderList', 'operate': 'update',
                        'dict': {'id':m_spider_id,'status': m_status}}}
    http.request(r'update', update)

'''
数据库操作：获取爬虫对应 model 的 key
'''


def load_model(m_spider_id):
    result = http.request(r'spider_model_query', {'spider_id': m_spider_id}).json()['base_key']
    return result


'''
进程操作: 刷新所有正在运行的 job
'''


def query_running_sid():
    # 获取所有正在运行和准备中的 job
    job_list = all_spiders('BASE_SPIDER')
    running_list = job_list['running'] + job_list['pending']
    running_jobs = []
    for rl in range(len(running_list)):
        job_id = running_list[rl]['id']
        running_jobs.append(job_id)

    # 将字典中的 job 与正在运行的 job 比较
    # 如果不存在，将其移除字典
    for i in list(spider_jobs):
        if spider_jobs[i].job_id not in running_jobs:
            spider_jobs.pop(i)


'''
数据库操作：获取所有spider信息，并重设其状态
'''


def reset_all_status():
    spider_list = load_spider_list()
    spiders = []
    for i in range(len(spider_list)):
        spider = {'id': spider_list[i].id, 'code': spider_list[i].code, 'name': spider_list[i].name,
                  'model_id': spider_list[i].model_id, 'status': spider_list[i].status,
                  'server_id': spider_list[i].server_id, 'server_name': spider_list[i].server_name,
                  'an_type': spider_list[i].an_type, 'is_auto': spider_list[i].is_auto,
                  'enable': spider_list[i].enable}
        if spider['id'] in spider_jobs.keys():
            spider['status'] = 'RUNNING'
        else:
            spider['status'] = 'STOP'
        upload_sub_spider(spider['id'], spider['status'])
        spiders.append(spider)
    return spiders
