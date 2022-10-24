# coding: utf-8
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.mysql import INTEGER, TEXT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from BaseSpider.settings import spid_engine

Base = declarative_base()
metadata = Base.metadata
Session = sessionmaker(bind=spid_engine)
session = Session()

class CrawlHistory(Base):
    __tablename__ = 'crawl_history'

    id = Column(VARCHAR(30), primary_key=True)
    spider_id = Column(VARCHAR(30), nullable=False, comment='启动的爬虫ID')
    crawl_aim_url = Column(TEXT, nullable=False, comment='爬取目标网址URl')
    redis_key = Column(VARCHAR(30), nullable=False)
    aim_crawl_num = Column(INTEGER(8), comment='本次预计爬取页面数')
    act_crawl_num = Column(INTEGER(8), comment='本次实际爬取页面数')
    server_id = Column(VARCHAR(30), nullable=False, comment='本次爬虫进程所属服务器ID')
    server_name = Column(VARCHAR(255), nullable=False, comment='本次爬虫进程所属服务器名')
    start_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime)
    result = Column(TEXT, comment='爬取统计结果')
    istrue_end = Column(VARCHAR(10), nullable=False, comment='是否正常结束标志')



# 新增
def add(item: CrawlHistory):
    if not isinstance(item, CrawlHistory):
        raise IndexError('数据类型不匹配')
    global session
    # 新增一条数据
    session.add(item)
    # 提交
    session.commit()
    # 关闭
    session.close()


# 删除
def delete(id):
    global session
    # 新增一条数据
    result = session.query(CrawlHistory).filter_by(id=(CrawlHistory.id if id is None else id)).delete()
    # 提交
    session.commit()
    # 关闭
    session.close()
    return result

# 查询
def query(id=None, spider_id=None):
    global session
    # 新增一条数据
    result = session.query(CrawlHistory).filter_by(id=(CrawlHistory.id if id is None else id),
                                                   spider_id=(CrawlHistory.spider_id if spider_id is None else spider_id)).all()
    # 关闭
    session.close()
    return result

# 获取上一次url
def query_latesturl(spider_id:str):
    global session
    # 新增一条数据
    result = session.query(CrawlHistory).filter_by(spider_id=spider_id).order_by(CrawlHistory.start_time.desc()).all()
    # 关闭
    session.close()
    if not result:
        return None
    else:
        return result[0].crawl_aim_url

# 获取上一次url
def query_latest_total_num(spider_id:str):
    global session
    # 新增一条数据
    result = session.query(CrawlHistory).filter_by(spider_id=spider_id).order_by(CrawlHistory.start_time.desc()).all()
    # 关闭
    session.close()
    if not result:
        return None
    else:
        return result[0].aim_crawl_num

# 获取上一次url
def query_total_num(spider_id:str):
    global session
    # 新增一条数据
    result = session.query(CrawlHistory).filter_by(spider_id=spider_id).order_by(CrawlHistory.start_time.desc()).all()
    # 关闭
    session.close()
    if not result:
        return 0
    else:
        total_num = 0
        for item in result:
            total_num += int(item.aim_crawl_num)
        return total_num

# 更新
def update(id: str, istrue_end, spider_id=None, crawl_aim_url=None,
           redis_key=None, aim_crawl_num=None, act_crawl_num=None, server_id=None
           , server_name=None, start_time=None, update_time=None, result=None):
    for item in session.query(CrawlHistory).filter(CrawlHistory.id == id):
        if spider_id is not None:
            item.spider_id = spider_id
        if crawl_aim_url is not None:
            item.crawl_aim_url = crawl_aim_url
        if redis_key is not None:
            item.redis_key = redis_key
        if aim_crawl_num is not None:
            item.aim_crawl_num = aim_crawl_num
        if act_crawl_num is not None:
            item.act_crawl_num = act_crawl_num
        if server_id is not None:
            item.server_id = server_id
        if server_name is not None:
            item.server_name = server_name
        if start_time is not None:
            item.start_time = start_time
        if update_time is not None:
            item.update_time = update_time
        if result is not None:
            item.result = result
        if istrue_end is not None:
            item.istrue_end = istrue_end
    session.commit()

