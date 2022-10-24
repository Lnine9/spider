from sqlalchemy import BigInteger, Column, TEXT, VARCHAR

from DataBaseOperate.data_operate.BaseTable import AnTable


class Attachment(AnTable):
    __tablename__ = 'attachment'

    id = Column(BigInteger(), primary_key=True)
    file_name= Column(VARCHAR(100), comment='附件名')
    file_type = Column(VARCHAR(10), comment='附件类型')
    file_size = Column(VARCHAR(30), comment='附件大小')
    url = Column(TEXT, comment='附件URL地址')
    local_path = Column(TEXT, comment='附件存储本地路径')

