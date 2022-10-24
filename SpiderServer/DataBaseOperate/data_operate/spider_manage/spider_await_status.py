import time

from sqlalchemy import Column, VARCHAR, TEXT
from sqlalchemy.dialects.mysql import INTEGER, DOUBLE, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from DataBaseOperate.setting import spid_engine

Base = declarative_base()
metadata = Base.metadata
Session = sessionmaker(bind=spid_engine)
session = Session()


class SpiderAwaitStatus(Base):
    __tablename__ = 'spider_await_status'

    id = Column(INTEGER, primary_key=True)
    spider_id = Column(INTEGER, nullable=False)
    aim_number = Column(INTEGER,comment='目标爬取总数')
    crawled_section_num = Column(INTEGER)
    crawled_announce_num = Column(INTEGER)
    complete_rate = Column(DOUBLE, comment='爬取完成率')
    status = Column(INTEGER, nullable=False)
    cur_offset = Column(INTEGER)
    end_time = Column(DATETIME)
    crawl_history_id = Column(VARCHAR(30))
    total_section = Column(INTEGER)
    latest_url = Column(TEXT, comment='上一段最新url')
    latest_time = Column(DATETIME)
    cur_time = Column(DATETIME)
    earliest_time = Column(DATETIME)



def query(spider_id=None):
    session = Session()
    # 新增一条数据
    result = session.query(SpiderAwaitStatus).filter_by(spider_id=(SpiderAwaitStatus.spider_id if spider_id is None else spider_id)).all()
    # 关闭
    session.close()
    return result[0]


def update(spider_id, crawled_section_num=None, crawled_announce_num=None, complete_rate=None,
           cur_offset=None, crawl_history_id=None, total_section=None):
    session = Session()
    for item in session.query(SpiderAwaitStatus).filter(SpiderAwaitStatus.spider_id == spider_id):
        if crawled_section_num is not None:
            item.crawled_section_num = crawled_section_num
        if crawled_announce_num is not None:
            item.crawled_announce_num = crawled_announce_num
        if complete_rate is not None:
            item.complete_rate = complete_rate
        if cur_offset is not None:
            item.cur_offset = cur_offset
        if crawl_history_id is not None:
            item.crawl_history_id = crawl_history_id
        if total_section is not None:
            item.total_section = total_section
        item.end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    session.commit()
    session.close()


def update_latest_url(spider_id, latest_url=None):
    session = Session()
    for item in session.query(SpiderAwaitStatus).filter(SpiderAwaitStatus.spider_id == spider_id):
        if latest_url is not None:
            item.latest_url = latest_url
    session.commit()
    session.close()

def update_complete_rate(spider_id, complete_rate):
    session = Session()
    for item in session.query(SpiderAwaitStatus).filter(SpiderAwaitStatus.spider_id == spider_id):
        if complete_rate is not None:
            item.complete_rate = complete_rate
    session.commit()
    session.close()


def update_aim_number(spider_id, aim_number=None):
    session = Session()
    for item in session.query(SpiderAwaitStatus).filter(SpiderAwaitStatus.spider_id == spider_id):
        if aim_number is not None:
            item.aim_number = aim_number
    session.commit()
    session.close()


def update_status(spider_id, status=None):
    session = Session()
    for item in session.query(SpiderAwaitStatus).filter(SpiderAwaitStatus.spider_id == spider_id):
        if status is not None:
            item.status = status
    session.commit()
    session.close()


def update_crawled_section_num(spider_id, crawled_announce_num=None):
    session = Session()
    for item in session.query(SpiderAwaitStatus).filter(SpiderAwaitStatus.spider_id == spider_id):
        if crawled_announce_num is not None:
            item.crawled_announce_num = crawled_announce_num
    session.commit()
    session.close()

def update_crawled_announce_num(spider_id, crawled_section_num=None):
    session = Session()
    for item in session.query(SpiderAwaitStatus).filter(SpiderAwaitStatus.spider_id == spider_id):
        if crawled_section_num is not None:
            item.crawled_section_num = crawled_section_num
    session.commit()
    session.close()