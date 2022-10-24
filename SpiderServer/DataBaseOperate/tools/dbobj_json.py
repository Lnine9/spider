from datetime import time,date

from DataBaseOperate.data_operate.BaseTable import BaseTable


def to_json(model):
    json_obj = {}
    if isinstance(model, BaseTable):
        for col in model._sa_class_manager.mapper.mapped_table.columns:
            json_obj[col.name] = getattr(model, col.name)
        return json_obj
    elif hasattr(model, 'to_json'):
        return getattr(model, 'to_json')()
    elif hasattr(model, '__dict__'):
        return model.__dict__
    else:
        return str(model)


def to_json_list(model_list):
    json_list = []
    for model in model_list:
        json_list.append(to_json(model))
    return json_list
