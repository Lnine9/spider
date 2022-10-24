from sqlalchemy.orm import sessionmaker

from DataBaseOperate.setting import spid_engine

DBSession = sessionmaker(bind=spid_engine)
session = DBSession()


def get_uuid_short():
    try:
        result = session.execute('select  UUID_SHORT() as uuid')
        for i in result:
            return i.uuid
    except:
        session.rollback()
        result = session.execute('select  UUID_SHORT() as uuid')
        for i in result:
            return i.uuid
