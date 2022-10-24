from sqlalchemy import Column, VARCHAR, TEXT, BigInteger

from BaseSpider.data_operate.BaseTable import AnTable


# 文件类
class FileList(AnTable):
    __tablename__ = 'file_list'

    id = Column(BigInteger(), primary_key=True)
    file_type = Column(VARCHAR(10), comment='文件类型')
    file_size = Column(VARCHAR(30), comment='文件大小')
    url = Column(TEXT, comment='文件URL地址')
    local_path = Column(TEXT, comment='文件存放本地地址')

FileList.create_table()