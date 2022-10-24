"""
关系解析器父类
"""
from abc import abstractmethod, ABC

from RelationAnalysis.server.central_control import CentralControl
from RelationAnalysis.data_operate import resolver as db
from RelationAnalysis.entity.announcement_info import AnnouncementInfoEntity


class BaseResolver(ABC):
    def __init__(self):
        self.order = None
        self.version = None

    def analysis_process(self, announcement_info: AnnouncementInfoEntity):
        """
        执行解析流程
        :param announcement_info:
        :return:
        """
        relation = self.analysis(announcement_info)  # 关系解析
        self.save_resolution_records(relation, announcement_info)  # 数据入库处理

    def save_resolution_records(self, relation, announcement_info: AnnouncementInfoEntity):
        """
        保存解析记录
        """
        # 关系入库
        relation = self.save_relation(relation)

        # 修改公告版本号
        announcement_info.relation_analysis_version = CentralControl.set_version(
            announcement_info.relation_analysis_version, order=self.order, version=self.version)
        # 修改公告信息
        self.modify_announcement_info(announcement_info, relation)

        # 写入记录
        self.save_records()

    def save_relation(self, relation):
        """
        关系入库
        """
        # 查询数据库是否存在该关系
        query_relation = self.query_relation(relation)

        if not query_relation:
            relation.id = db.save_relation(relation)
            return relation
        else:
            return query_relation

    def query_relation(self, relation):
        """
        判断该关联是否存在
        :param relation:
        :return:
        """
        sql = self.query_exist_relation_sql(relation)
        return db.do_sql(sql)

    def save_records(self):
        # todo 生成records并入库
        db.write_records('records')

    @abstractmethod
    def analysis(self, announcement_info: AnnouncementInfoEntity):
        """
        解析
        """
        pass

    @abstractmethod
    def modify_announcement_info(self, announcement, relation):
        """
        修改公告信息
        :param announcement:
        :param relation:
        :return:
        """
        pass

    @abstractmethod
    def query_exist_relation_sql(self, relation):
        """
        select count(*) from xx where xxx=xxx
        :param relation:
        :return:
        """
        return ""
