# coding=utf8
import threading
from datetime import datetime
from enum import Enum
from SpiderClient.entity.spider_job import SpiderJob
from SpiderClient.service import init_param, m_scrapyd, spider_jobs


class SpiderInfo:
    """
    爬虫信息管理
    """
    spider_id: str
    name: str  # 名字
    redis_key: str  # redis_key

    spider_await_time: int = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class CrawlerTaskUnitStatus(Enum):
    SLEEP = 'sleep_list'
    READY = 'ready_queue'
    RUNNING = 'run_list'


class CrawlerTaskUnit:
    """
    爬虫任务单元
    """
    spider_info: SpiderInfo = None
    spider_job_id: str = None
    has_next: bool = True
    spider_stop_time: datetime = None
    status: CrawlerTaskUnitStatus = None

    def run_spider(self):
        self.launching(self.spider_info.spider_id)

    @staticmethod
    def launching(spider_id):
        # 向 redis 发送参数
        param = init_param.param_to_redis(spider_id)
        if not param['status']:
            return {'state': 300, 'error': str(param['error'])}
        m_job_id = m_scrapyd.schedule('BASE_SPIDER', 'BASE_SPIDER', id=spider_id)
        m_spider_job = SpiderJob(spider_id=spider_id, job_id=m_job_id, status='running')
        spider_jobs[spider_id] = m_spider_job
        return {'state': 200, 'pid': m_job_id}


class PendingList:
    _instance_lock = threading.Lock()
    ready_queue = []
    sleep_list = []
    run_list = []
    all_task = {}

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with PendingList._instance_lock:
                if not hasattr(cls, '_instance'):
                    PendingList._instance = super().__new__(cls)
        return PendingList._instance

    def add_task(self, crawler_task_unit: CrawlerTaskUnit):
        """
        添加任务到就绪队列
        :param crawler_task_unit:
        :return:
        """
        if self.all_task.get(str(crawler_task_unit.spider_info.spider_id), None) is None:
            # 直接加入就绪队列
            crawler_task_unit.status = CrawlerTaskUnitStatus.READY
            self.ready_queue.append(crawler_task_unit)
            self.all_task.setdefault(str(crawler_task_unit.spider_info.spider_id), crawler_task_unit)

    def delete_task(self, crawler_task_unit: CrawlerTaskUnit, forcibly=False):
        """
        删除任务
        :param forcibly: 强制删除，即时在运行队列中
        :param crawler_task_unit:
        :return:
        """
        if crawler_task_unit is not None:
            if crawler_task_unit.status == CrawlerTaskUnitStatus.RUNNING and not forcibly:
                crawler_task_unit.has_next = False
            elif crawler_task_unit.status == CrawlerTaskUnitStatus.RUNNING and not forcibly:
                self.run_list.remove(crawler_task_unit)
            elif crawler_task_unit.status == CrawlerTaskUnitStatus.SLEEP:
                self.sleep_list.remove(crawler_task_unit)
            elif crawler_task_unit.status == CrawlerTaskUnitStatus.READY:
                self.ready_queue.remove(crawler_task_unit)
            del self.all_task[str(crawler_task_unit.spider_info.spider_id)]

    def mission_accomplished(self, crawler_task_unit: CrawlerTaskUnit):
        """
        任务完成一次
        :param crawler_task_unit:
        :return:
        """
        if crawler_task_unit in self.run_list:  # 任务处于运行队列
            self.run_list.remove(crawler_task_unit)  # 从运行队列移除任务
            if crawler_task_unit.has_next:  # 判断任务是否继续
                # 加入随眠列表
                self.sleep_list.append(crawler_task_unit)
                crawler_task_unit.spider_stop_time = datetime.now()
                crawler_task_unit.status = CrawlerTaskUnitStatus.SLEEP

    def get_task(self, number=1):
        """
        获得任务
        :param number:
        :return:
        """
        tasks = []
        for i in range(number):
            if len(self.ready_queue) > 0:
                task = self.ready_queue.pop(0)
                task.status = CrawlerTaskUnitStatus.RUNNING  # 改为运行态
                self.run_list.append(task)  # 加入运行队列
                tasks.append(task)
            else:  # 就绪队列为空
                break
        return tasks

    def reload_task(self):
        """
        检查并重设睡眠任务
        :return:
        """
        now = datetime.now()  # 当前时间
        for task in self.sleep_list:
            if not task.spider_info.spider_await_time \
                    or task.spider_info.spider_await_time >= (now - task.spider_stop_time).seconds:
                # 将任务移入就绪队列
                self.sleep_list.remove(task)
                self.ready_queue.append(task)
                task.status = CrawlerTaskUnitStatus.READY

    def clear(self):
        self.run_list = []
        self.ready_queue = []
        self.sleep_list = []
        self.all_task = {}


class SchedulerInfo(object):
    _instance_lock = threading.Lock()

    write_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with SchedulerInfo._instance_lock:
                if not hasattr(cls, '_instance'):
                    SchedulerInfo._instance = super().__new__(cls)
        return SchedulerInfo._instance

    project_name = 'BASE_SPIDER'
    max_spider_number = 1
    bg_scheduler = None
