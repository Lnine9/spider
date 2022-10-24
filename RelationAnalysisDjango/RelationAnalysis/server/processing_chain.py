from RelationAnalysis.data_operate.connection_server import DBService
from RelationAnalysis.server import add_check, repeat_check
from RelationAnalysis.tool.logging import logger
from RelationAnalysis.server.hitsory_processor import create_history


def repeat_check_control(relations):
    return repeat_check.check_having(relations)


def serialization(relations):
    all_items = []

    all_items += get_deal_dicts(relations.get('add', []), 'add')

    all_items += get_deal_dicts(relations.get('update', []), 'update')

    history = relations.get('history')
    if isinstance(history, dict):
        history = create_history(**history)
    elif isinstance(history, list):
        history = [create_history(**h) for h in history]
    else:
        logger.warning(f"历史记录({type(history)})未入库")

    all_items += get_deal_dicts(history, 'add')
    return all_items


def get_deal_dicts(objs, operate_type):
    deal_items = []
    if objs:
        for obj in objs:
            if obj:
                item = DBService.get_deal_item(obj.class_type, obj.__class__.__name__, operate_type, obj)
                deal_items.append(item)
    return deal_items


processings = [repeat_check_control, ]


def chains(relations):
    if 'add' not in relations.keys():
        relations.setdefault('add', [])
    if 'update' not in relations.keys():
        relations.setdefault('update', [])
    for processing in processings:
        relations = processing(relations)
    return serialization(relations)
