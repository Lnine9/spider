# coding: utf-8
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR
from DataBaseOperate.data_operate.BaseTable import SMTable


class GroupSpiderRel(SMTable):
    """
     分布式--分组爬虫关联表
     """
    __tablename__ = 'group_spider_rel'

    id = Column(VARCHAR(30), primary_key=True)
    spider_id = Column(VARCHAR(50), nullable=False, comment='爬虫ID')
    group_id = Column(VARCHAR(50), nullable=False, comment='分组ID')

    # 查询
    @staticmethod
    def queryspiderid(group_id):
        session = GroupSpiderRel.getSession()
        # 新增一条数据
        result = session.query(GroupSpiderRel).filter_by(group_id=group_id).all()
        # 关闭
        session.close()
        return result
