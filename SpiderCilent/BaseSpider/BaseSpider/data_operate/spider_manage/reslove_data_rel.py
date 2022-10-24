from sqlalchemy import Column, BigInteger
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER
from BaseSpider.data_operate.BaseTable import SMTable


class ResloveDataRel(SMTable):
    """
    response解析数据关联表
    """
    __tablename__ = 'resolve_data_rel'
    id = Column(BigInteger(), primary_key=True)
    spider_id = Column(VARCHAR(30), nullable=False, comment='爬虫ID')
    response_id = Column(BigInteger(), nullable=False, comment='response数据_id')
    version_no = Column(VARCHAR(255), comment='解析使用的版本号')
    priority = Column(INTEGER(10), comment='使用的解析器优先级', default=1)
    type = Column(VARCHAR(20), comment='公告类型')
    an_id = Column(BigInteger(), comment='公告id')

    # 查询
    def query_object(response_id=None):
        return ResloveDataRel.query(response_id=response_id)




