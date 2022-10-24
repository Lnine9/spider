from sqlalchemy import Column, BigInteger, VARCHAR

from DataBaseOperate.data_operate.BaseTable import RelTable


class AnRelationAnalysisVersion(RelTable):
    """
    公告关系版本版本库
    """
    __tablename__ = 'an_relation_analysis_version'

    id = Column(BigInteger(), primary_key=True)
    an_id = Column(BigInteger())
    an_type = Column(VARCHAR(20))
    relation_analysis_version = Column(VARCHAR(255))
    real_version = Column(VARCHAR(255))

# AnRelationAnalysisVersion.create_table()
