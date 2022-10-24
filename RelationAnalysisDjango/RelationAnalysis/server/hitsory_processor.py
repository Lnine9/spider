import time

from RelationAnalysis.data_operate.pool_table import RelTable
from RelationAnalysis.data_operate.relation_analysis.resolve_history import ResolveHistory


def update_history(resolver_history, resolver_id, announcement_id, relation_id):
    resolver_history[0].parsing_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    resolver_history[0].relation_type = resolver_id
    resolver_history[0].announcement_id = announcement_id
    resolver_history[0].relation_id = relation_id
    resolver_history[0].update_self()


def create_history(resolver_id, announcement_id, relation):
    if isinstance(relation, list) or isinstance(relation, tuple):
        ids = []
        for one in relation:
            ids.append(str(getattr(one, 'id', getattr(one, 'Id', None))))
        relation = {id: ','.join(ids)}
    relation_id = getattr(relation, 'id', getattr(relation, 'Id', None))
    resolver_history = ResolveHistory()
    resolver_history.id = RelTable.UUID_SHORT()
    resolver_history.parsing_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    resolver_history.relation_type = resolver_id
    resolver_history.announcement_id = announcement_id
    resolver_history.relation_id = relation_id
    resolver_history.add_self()
