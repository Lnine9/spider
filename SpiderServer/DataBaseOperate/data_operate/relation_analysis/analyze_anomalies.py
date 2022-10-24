from sqlalchemy import Column, BigInteger, INTEGER, VARCHAR, TEXT

from DataBaseOperate.data_operate.BaseTable import RelTable


class AnalyzeAnomalies(RelTable):
    """
    分析异常
    """
    __tablename__ = 'analyze_anomalies'

    id = Column(INTEGER, primary_key=True)
    announcement_id = Column(BigInteger, comment='公告id')
    announcement_type = Column(VARCHAR(20), comment='公告类型')
    error_type = Column(VARCHAR(255), comment='错误类型')
    error_message = Column(TEXT, comment='错误信息')
    resolver_id = Column(VARCHAR(20), comment='解析器id')
    abnormal_time = Column(VARCHAR(20), comment='异常时间')


