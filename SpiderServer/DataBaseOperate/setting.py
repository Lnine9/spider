from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
anno_engine = create_engine("mysql+mysqlconnector://root:l20020204@localhost/announcement?charset=utf8mb4&collation=utf8mb4_general_ci&auth_plugin=mysql_native_password", pool_size=10, max_overflow=10)  # 连接数据库
spid_engine = create_engine("mysql+mysqlconnector://root:l20020204@localhost/spider_manage?charset=utf8mb4&collation=utf8mb4_general_ci&auth_plugin=mysql_native_password", pool_size=10, max_overflow=10)  # 连接数据库
rel_engine = create_engine("mysql+mysqlconnector://root:l20020204@localhost/relation_analysis?charset=utf8mb4&collation=utf8mb4_general_ci", pool_size=1, max_overflow=1)
# hanxin2001
