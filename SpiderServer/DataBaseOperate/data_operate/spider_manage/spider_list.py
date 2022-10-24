# coding: utf-8
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, TEXT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from DataBaseOperate.data_operate.BaseTable import SMTable
from DataBaseOperate.setting import spid_engine

Base = declarative_base()
metadata = Base.metadata
Session = sessionmaker(bind=spid_engine)
session = Session()


class SpiderList(SMTable, Base):
    __tablename__ = 'spider_list'

    id = Column(VARCHAR(30), primary_key=True, nullable=False)
    code = Column(VARCHAR(5), primary_key=True, nullable=False, comment='爬虫识别代号')
    name = Column(VARCHAR(40), primary_key=True, nullable=False, comment='爬虫名，启动者自定义，不可重名')
    model_id = Column(VARCHAR(30), nullable=False, comment='所选模板ID')
    status = Column(VARCHAR(8), nullable=False, comment='')
    server_id = Column(VARCHAR(30), nullable=False, comment='所属服务器ID')
    server_name = Column(VARCHAR(255), comment='所属服务器名')
    an_type = Column(VARCHAR(10),nullable=False,comment='公告所属表  CB_G: call_bid_government,WB_G: win_bid_government,FB_G: failure_bid_government,MB_G: modify_bid_government,CB_E: call_bid_engineering')
    is_auto = Column(VARCHAR(5),nullable=False,  comment='是否自启动')
    enable = Column(VARCHAR(10),nullable=False,  comment='是否能启动')
	
# 新增
def add(item: SpiderList):
    if not isinstance(item, SpiderList):
        raise IndexError('数据类型不匹配')
    global session
    # 新增一条数据
    session.add(item)
    # 提交
    session.commit()
    # 关闭
    session.close()


# 删除
def delete(id=None, code=None):
    global session
    # 新增一条数据
    result = session.query(SpiderList).filter_by(id=(SpiderList.id if id is None else id),
                                                 code=(SpiderList.code if code is None else code)).delete()
    # 提交
    session.commit()
    # 关闭
    session.close()
    return result


# 查询
def query(id=None, code=None, model_id = None):
    global session
    # 新增一条数据
    result = session.query(SpiderList).filter_by(id=(SpiderList.id if id is None else id),
                                                 code=(SpiderList.code if code is None else code),
                                                 model_id=(SpiderList.model_id if model_id is None else model_id)).all()
    # 关闭
    session.close()
    return result


def queryid(model_id = None):
    global session
    # 新增一条数据
    result = session.query(SpiderList).filter_by(model_id=(SpiderList.model_id if model_id is None else model_id)).all()
    # 关闭
    session.close()
    return result[0].id

# 更新
def update(id: str, code=None, name=None,
           model_id=None, status=None, server_id=None, server_name=None):
    for item in session.query(SpiderList).filter(SpiderList.id == id):
        if code is not None:
            item.code = code
        if name is not None:
            item.name = name
        if model_id is not None:
            item.model_id = model_id
        if status is not None:
            item.status = status
        if server_id is not None:
            item.server_id = server_id
        if server_name is not None:
            item.server_name = server_name
    session.commit()
