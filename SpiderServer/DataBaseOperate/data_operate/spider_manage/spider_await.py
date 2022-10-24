from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from DataBaseOperate.setting import spid_engine

Base = declarative_base()
metadata = Base.metadata
Session = sessionmaker(bind=spid_engine)
session = Session()


class SpiderAwait(Base):
    __tablename__ = 'spider_await'

    id = Column(INTEGER, primary_key=True)
    spider_id = Column(INTEGER, nullable=False, comment='所属爬虫ID')
    await_minute = Column(INTEGER, nullable=False)
    section_page_size = Column(INTEGER, nullable=False, comment='')

def query(spider_id=None):
    global session
    # 新增一条数据
    result = session.query(SpiderAwait).filter_by(spider_id=(SpiderAwait.spider_id if spider_id is None else spider_id)).all()
    # 关闭
    session.close()
    return result[0]