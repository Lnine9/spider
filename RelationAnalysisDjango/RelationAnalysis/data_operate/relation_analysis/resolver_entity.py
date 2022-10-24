from sqlalchemy import Column, BigInteger, VARCHAR, TEXT, INTEGER

from RelationAnalysis.data_operate.pool_table import RelTable

"""
供应商类
"""


class ResolverEntity(RelTable):
    __tablename__ = 'resolver_entity'

    id = Column(VARCHAR(30), primary_key=True)
    name = Column(VARCHAR(50), comment='解析器名称')
    class_path = Column(TEXT(), comment='解析器全路径类名')
    version_no = Column(VARCHAR(30), comment='版本')
    order = Column(INTEGER, comment='解析器序号')
    immediate = Column(INTEGER, comment='是否为及时解析')
    relation_type = Column(VARCHAR(255), comment='描述解析器解析类型')
    table_type = Column(VARCHAR(20), comment='传入表类型')
    take_effect = Column(INTEGER, comment='是否启用')
    pre_parser = Column(VARCHAR(255))

    def __init__(self, id=None, name=None, class_path=None, version_no='00', order=0, immediate=0, relation_type="",
                 table_type="", pre_parser=None):
        self.id = id
        self.name = name
        self.class_path = class_path
        self.version_no = version_no
        self.order = order
        self.immediate = immediate
        self.relation_type = relation_type
        self.table_type = table_type
        if pre_parser is None:
            pre_parser = ""
        self.pre_parser = [i for i in pre_parser.split(",") if i]

# ResolverEntity.create_table()
