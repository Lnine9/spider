from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, TEXT, DOUBLE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from DataBaseOperate.setting import spid_engine

Base = declarative_base()
metadata = Base.metadata
Session = sessionmaker(bind=spid_engine)
session = Session()

class SubComponent(Base):
    __tablename__ = 'sub_component'

    id = Column(VARCHAR(30), primary_key=True)
    parent_component_id = Column(VARCHAR(20), nullable=False)
    component_sequence = Column(INTEGER, nullable=False, comment='序列')
    version_no = Column(VARCHAR(30), comment='版本号')
    type = Column(VARCHAR(20), nullable=False, comment='类型')
    name = Column(VARCHAR(50), comment="组件名")
    class_path = Column(TEXT, comment="类路径")
    utilization_rate = Column(DOUBLE, comment="使用率")
    description = Column(TEXT, comment="描述")

# 查询
def query():
    session = Session()
    # 新增一条数据
    result = session.query(SubComponent).all()
    # 关闭
    session.close()
    return result

def query_parent_id(parent_component_id=None):
    session = Session()

    result = session.query(SubComponent). \
        filter_by(parent_component_id=(SubComponent.parent_component_id if parent_component_id is None else parent_component_id)). \
        order_by(SubComponent.component_sequence.asc()).all()
    # 关闭
    session.close()
    return result