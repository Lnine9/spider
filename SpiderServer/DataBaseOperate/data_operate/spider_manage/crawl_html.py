import logging

from sqlalchemy import BigInteger, Column, VARCHAR
from sqlalchemy.dialects.mysql import MEDIUMTEXT, INTEGER
from DataBaseOperate.data_operate.BaseTable import SMTable
from DataBaseOperate.data_operate.spider_manage.crawl_an_rel import CrawlAnRel


class CrawlHtml(SMTable):
    """
     resposne数据表
     """
    __tablename__ = 'crawl_html'

    id = Column(BigInteger(), primary_key=True)
    spider_id = Column(VARCHAR(30), nullable=False, comment='爬虫id')
    url = Column(VARCHAR(500), nullable=False, comment='网页URL')
    content = Column(MEDIUMTEXT, nullable=False, comment='response请求页面内容')
    type = Column(VARCHAR(20), nullable=False, comment='公告类型')
    section = Column(INTEGER, comment='对应段')

    logging.getLogger().setLevel(logging.INFO)

    # 查询
    @staticmethod
    def query_ById(id):
        return CrawlHtml.query(id=id)[0]


    # 未解析：0  已解析：解析时的父组件版本号，一次解析数量为1000
    @staticmethod
    def query_BySpiderID(spider_id, section):
        session = CrawlHtml.getSession()
        result = session.query(CrawlHtml.id).filter_by(spider_id=spider_id, section=section).limit(1000).all()
        session.commit()
        # 关闭
        session.close()
        return result

    @staticmethod
    def updates(spider_id, section):
        list = CrawlHtml.query(spider_id=spider_id, section=section)
        CrawlHtml.update_all(items=list, section='0')


    @staticmethod
    def update_section(id,section):
        CrawlHtml.update(id, {"section": section})


    @staticmethod
    def query_section_need_delete(spider_id, section):
        session = CrawlHtml.getSession()
        result = session.query(CrawlHtml).filter_by(spider_id=(CrawlHtml.spider_id if spider_id is None else spider_id),
                                                    section=section).all()
        len = 0
        for item in result:
            res_id = item.id
            session.delete(item)
            CrawlHtml.delete_rel(res_id)
            len += 1
            logging.info('delete one record  already deleted ' + str(len))
        session.commit()
        # 关闭
        session.close()

    @staticmethod
    def delete_rel(response_id):
        session = CrawlHtml.getSession()
        # 新增一条数据
        result = session.query(CrawlAnRel).filter_by(response_id=response_id).delete()
        # 提交
        session.commit()
        # 关闭
        session.close()

    @staticmethod
    def query_by_url(spider_id=None, url=None):
        session = CrawlHtml.getSession()
        result = session.query(CrawlHtml).filter_by(spider_id=(CrawlHtml.spider_id if spider_id is None else spider_id),
                                                    url=url).all()
        session.commit()
        # 关闭
        session.close()
        return result


