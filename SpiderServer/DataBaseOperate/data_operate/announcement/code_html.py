from sqlalchemy import BigInteger, Column, TEXT, VARCHAR
from sqlalchemy.dialects.mysql import MEDIUMTEXT

from DataBaseOperate.data_operate.BaseTable import AnTable


class CodeHtml(AnTable):
    __tablename__ = 'code_html'

    id = Column(BigInteger(), primary_key=True)
    file_type = Column(VARCHAR(10), comment='文件类型')
    file_size = Column(VARCHAR(30), comment='文件大小')
    url = Column(TEXT, comment='文件URL')
    local_path = Column(TEXT, comment='本地地址')
    code = Column(MEDIUMTEXT, comment='页面代码')
