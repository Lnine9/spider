from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from RelationAnalysis.data_operate.connection_server import ClassType
from RelationAnalysis.data_operate.base_server_table import BaseServerTable

BaseTable = BaseServerTable


class AnTable(BaseTable, declarative_base(create_engine("mysql+mysqlconnector://username:password@ip/announcement"))):
    """
    连接爬取公告数据库
    """
    __abstract__ = True
    class_type = ClassType.ANNOUNCEMENT


class SMTable(BaseTable, declarative_base(create_engine("mysql+mysqlconnector://username:password@ip/spider_manage"))):
    """
    连接爬虫管理系统数据库
    """
    __abstract__ = True
    class_type = ClassType.SPIDER_MANAGE


class RelTable(BaseTable,
               declarative_base(create_engine("mysql+mysqlconnector://username:password@ip/analysis_relation"))):
    """
    连接公告关系解析数据库
    """
    __abstract__ = True
    class_type = ClassType.RELATION_ANALYSIS
