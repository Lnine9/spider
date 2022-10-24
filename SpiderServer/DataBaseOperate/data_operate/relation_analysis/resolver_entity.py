from sqlalchemy import Column, VARCHAR, TEXT, INTEGER

from DataBaseOperate.data_operate.BaseTable import RelTable


class ResolverEntity(RelTable):
    """
    供应商类
    """
    __tablename__ = 'resolver_entity'

    id = Column(VARCHAR(30), primary_key=True)
    name = Column(VARCHAR(50), comment='解析器名称')
    class_path = Column(TEXT(), comment='解析器全路径类名')
    version_no = Column(VARCHAR(30), comment='版本')
    order = Column(INTEGER)
    immediate = Column(INTEGER)
    relation_type = Column(VARCHAR(255))
    take_effect = Column(INTEGER, comment='是否启用')
    pre_parser = Column(VARCHAR(255))
