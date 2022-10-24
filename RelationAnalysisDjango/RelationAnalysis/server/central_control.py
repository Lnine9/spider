from enum import Enum

from apscheduler.schedulers.background import BackgroundScheduler

from RelationAnalysis.entity.exceptions import RecordException
from RelationAnalysis.server.processing_chain import chains
from RelationAnalysis.tool.logging import logger
from RelationAnalysis.tool.class_reflection import instantiation_by_path, dictionary_assignment
from RelationAnalysis.data_operate.connection_server import DBService
from RelationAnalysis.data_operate import control as db
from RelationAnalysis.data_operate.relation_analysis.analyze_anomalies import AnalyzeAnomalies


class CentralControl:
    scheduler = BackgroundScheduler()  # 定时器

    def __init__(self):
        self.resolvers = {}  # 所有解析器实例
        self.immediate_resolvers = {}  # 即时解析使用的实例
        self.latest_version = {}  # 最新版本号
        self.immediate_version = {}
        self.loading_resolvers()  # 加载解析器

    def loading_resolvers(self):
        """
        加载解析器
        :return:
        """
        # 载入解析器
        for resolver in db.get_resolvers():
            resolver_obj = instantiation_by_path('RelationAnalysis.' + resolver.class_path)
            dictionary_assignment(resolver_obj,
                                  {'id': resolver.id, 'version': resolver.version_no, 'order': resolver.order,
                                   'relation_type': resolver.relation_type, 'pre_parser': resolver.pre_parser})
            # 加载所有解析器
            if resolver.table_type not in self.resolvers.keys():
                self.resolvers[resolver.table_type] = {}
            self.resolvers[resolver.table_type][str(resolver_obj.order)] = resolver_obj

            # 初始化版本号
            self.latest_version[resolver.table_type] = self.set_version(
                self.latest_version.get(resolver.table_type, ''),
                resolver.order, resolver.version_no)

            # 即时解析器列表
            if resolver.immediate == 1:
                if not hasattr(self.immediate_resolvers, resolver.table_type):
                    self.immediate_resolvers[resolver.table_type] = {}
                self.immediate_resolvers[resolver.table_type][str(resolver_obj.order)] = resolver_obj

                self.immediate_version[resolver.table_type] = self.set_version(
                    self.immediate_version.get(resolver.table_type, ''),
                    resolver.order, resolver.version_no)

        #  前置解析器处理，生成前置解析版本号
        for type_resolvers in self.resolvers.values():
            for resolver_obj in type_resolvers.values():
                if getattr(resolver_obj, "pre_parser"):
                    pre_parser_version = ''
                    for parse_id in getattr(resolver_obj, "pre_parser"):
                        pre_parser = type_resolvers.get(str(parse_id))
                        pre_parser_version = self.set_version(pre_parser_version,
                                                              getattr(pre_parser, 'order'),
                                                              getattr(pre_parser, 'version'))
                    setattr(resolver_obj, 'pre_parser', pre_parser_version)

    def resolver(self, announcement, resolver_type=None, an_type=None):
        """
        公告执行解析
        :param an_type: 公告类型
        :param announcement:公告实体
        :param resolver_type:公告解析方式：即时解析、定时任务
        :return:
        """
        version = db.get_relation_analysis_version(announcement.id, an_type, announcement.class_type)  # 获得公告版本号

        # 通过解析方式获取解析版本号
        if resolver_type == RelationType.schedule:
            need_version = self.latest_version.get(an_type, "")
        elif resolver_type == RelationType.immediate:
            need_version = self.immediate_version.get(an_type, "")
        else:
            need_version = ''

        # 获取目标解析器列表
        resolvers = self.resolvers.get(an_type)

        for order in range(1, len(need_version) // 2 + 1):  # 遍历解析器
            if not CentralControl.check_order_version(version, need_version, order):  # 当前解析器需要执行分析
                resolver = resolvers.get(str(order), None)  # 获取解析器
                if not resolver.pre_parser or CentralControl.check_version(version, resolver.pre_parser):  # 前置分析解析器有效执行
                    try:
                        relations = resolver.analysis(announcement)  # 执行分析操作
                    except Exception as e:
                        logger.warning(f'解析器异常, 关联解析跳过，解析器id：{resolver.id}', exc_info=True)
                        AnalyzeAnomalies(announcement_id=announcement.id, announcement_type=an_type,
                                         error_type='解析器异常', resolver_id=resolver.id,
                                         error_message=str(e.args)).add_self()
                    else:
                        try:
                            all_items = CentralControl.data_processing(relations)  # 数据加工
                        except Exception as e:
                            logger.warning(f'数据处理异常, 关联解析跳过，解析器id：{resolver.id}', exc_info=True)
                            AnalyzeAnomalies(announcement_id=announcement.id, announcement_type=an_type,
                                             error_type='数据处理异常', resolver_id=resolver.id,
                                             error_message=str(e.args)).add_self()
                        else:
                            try:
                                CentralControl.data_storage(all_items)  # 数据入库
                            except RecordException as recordException:
                                # logger.warning(f'数据入库异常, 关联解析跳过，解析器id：{resolver.id}', exc_info=True)
                                AnalyzeAnomalies(announcement_id=announcement.id, announcement_type=an_type,
                                                 error_type=recordException.name, resolver_id=resolver.id,
                                                 error_message=str(recordException.args)).add_self()
                            except Exception as e:
                                logger.warning(f'数据入库异常, 关联解析跳过，解析器id：{resolver.id}', exc_info=True)
                                AnalyzeAnomalies(announcement_id=announcement.id, announcement_type=an_type,
                                                 error_type='数据入库异常', resolver_id=resolver.id,
                                                 error_message=str(e.args)).add_self()
                            else:
                                version = self.set_version(version, resolver.order, resolver.version)  # 更新当前公告版本号

                                db.update_relation_analysis(announcement_id=announcement.id,
                                                            relation_analysis_version=version,
                                                            real_version=version,
                                                            an_type=an_type,
                                                            class_type=announcement.class_type)  # 数据库更新当前公告版本号
                else:
                    logger.warning(
                        f'分析跳过: 公告id：{announcement.id}, 前置解析器异常：当前版本号为 {version}，需求前置版本号为 {resolver.pre_parser}')
                    # 记录数据入库异常
                    AnalyzeAnomalies(announcement_id=announcement.id, announcement_type=an_type,
                                     error_type='分析跳过', resolver_id=resolver.id,
                                     error_message=f'前置解析器异常：当前版本号为 {version}，需求前置版本号为 {resolver.pre_parser}').add_self()
        new_version = CentralControl.update_version(version, need_version)  # 解析完成，更新版本号
        if version != new_version:  # 当前版本号与最新存在差异，保存最新版本号
            db.update_relation_analysis(announcement_id=announcement.id, relation_analysis_version=new_version,
                                        an_type=an_type, class_type=announcement.class_type)  # 数据库更新当前公告版本号
        return announcement

    def get_version(self, resolver_type=None, an_type=None):
        if resolver_type == RelationType.schedule:
            an_version = self.latest_version.get(an_type, '')
            an_version = self.immediate_version.get(an_type, '')
        else:
            return

        regexp = '^'
        for i in range(0, len(an_version), 2):
            now = an_version[i:i + 2]
            if now == '00':
                regexp += '.{2}'
            else:
                regexp += now
        return regexp

    @staticmethod
    def set_version(old_version: str, order: int, version: str):
        """
        版本号生成方法
        :param old_version:
        elif resolver_type == RelationType.immediate:
        :param order:
        :param version:
        :return:
        """
        if not version:
            version = ''
        else:
            version = str(version)
        if not old_version:
            old_version = ''
        else:
            old_version = str(old_version)

        if len(version) != 2:
            logger.error('解析器版本号长度错误：' + version)
            raise ValueError('version 长度错误：' + version)
        if order < 1:
            logger.error('解析器序号错误：' + version)
            raise ValueError('order 值错误：' + str(order))

        need = (order - 1) * 2 - len(old_version)  # 计算长度差值
        if need > 0:
            old_version += '0' * need  # 补充差位
        # 替换指定位的值
        return old_version[:(order - 1) * 2] + version + old_version[order * 2:]

    @staticmethod
    def update_version(old_version: str, new_version: str):
        """
        更新版本号
        :param old_version:
        :param new_version:
        :return:
        """
        if not old_version:
            return new_version

        old_version = str(old_version)
        new_version = str(new_version)
        for order in range(1, len(new_version) // 2 + 1):
            if new_version[(order - 1) * 2:order * 2] \
                    and new_version[(order - 1) * 2:order * 2] not in ['00', old_version[(order - 1) * 2:order * 2]]:
                old_version = old_version[:(order - 1) * 2] + new_version[(order - 1) * 2:order * 2] \
                              + old_version[order * 2:]
        return old_version

    @staticmethod
    def check_version(now_version: str, need_version: str):
        """
        整体版本号比较
        :param now_version:
        :param need_version:
        :return:
        """
        now_version = str(now_version)
        need_version = str(need_version)
        for order in range(1, len(need_version) // 2 + 1):
            check_one = CentralControl.check_order_version(now_version=now_version, need_version=need_version,
                                                           order=order)
            if not check_one:
                return False
        return True

    @staticmethod
    def check_order_version(now_version: str, need_version: str, order: int):
        """
        指定序号版本号比较
        :param order:
        :param now_version:
        :param need_version:
        :return:
        """
        now_version = str(now_version)
        need_version = str(need_version)
        index = (order - 1) * 2
        resolver_version = need_version[index:index + 2]
        if (not now_version or now_version[index:index + 2] != resolver_version) \
                and (not resolver_version or resolver_version != '00'):
            return False
        return True

    @staticmethod
    def data_processing(relations):
        """
        数据加工操作
        :param relations:
        :return:
        """
        if relations:
            return chains(relations)

    @staticmethod
    def data_storage(all_items):
        """
        统一数据入库
        :param all_items:
        :return:
        """
        if all_items:
            DBService.deal_operate(all_items)

    @classmethod
    def schedule_start(cls):
        """
        启动定时任务
        :return:
        """
        if cls.scheduler.state == 0:
            cls.scheduler.start()

    @classmethod
    def schedule_stop(cls):
        """
        停止定时任务
        :return:
        """
        if cls.scheduler.state != 0:
            cls.scheduler.shutdown()

    @classmethod
    def pause_job(cls, job_id):
        cls.scheduler.pause_job(job_id)

    @classmethod
    def add_job(cls, job_id, method, trigger='interval', **kwargs):
        for job in cls.scheduler.get_jobs():
            if job.id == job_id:
                if cls.scheduler.state == 0:
                    cls.scheduler.start()
                else:
                    cls.scheduler.resume_job(job_id)
                return
        cls.scheduler.add_job(method, id=job_id, trigger=trigger, replace_existing=True, **kwargs)

    @classmethod
    def delete_job(cls, job_id):
        cls.scheduler.remove_job(job_id)

    @classmethod
    def modify_interval(cls, job_id, trigger='interval', **kwargs):
        """
        修改任务属性
        :param job_id:
        :param trigger:
        :param kwargs: 其他常用定时设置：minutes
        :return:
        """
        cls.scheduler.reschedule_job(job_id, trigger=trigger, **kwargs)


class RelationType(Enum):
    """
    控制器启动方式枚举
    """
    schedule = 1  # 定时任务
    immediate = 2  # 即时处理
