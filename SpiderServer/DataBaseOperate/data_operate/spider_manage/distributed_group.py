# coding: utf-8
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR
from DataBaseOperate.data_operate.BaseTable import SMTable


class DistributedGroup(SMTable):
    """
     分布式--口令分组表
     """
    __tablename__ = 'distributed_group'

    id = Column(VARCHAR(30), primary_key=True)
    group_name = Column(VARCHAR(50), nullable=False, comment='组名')

    # 查询
    @staticmethod
    def queryid(group_name):
        session = DistributedGroup.getSession()
        # 新增一条数据
        result = session.query(DistributedGroup).filter_by(group_name=group_name).all()
        # 关闭
        session.close()
        return result
