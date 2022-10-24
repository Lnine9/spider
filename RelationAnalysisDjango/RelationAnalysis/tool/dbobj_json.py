def to_json(model):
    if hasattr(model, 'to_json'):
        return getattr(model, 'to_json')()
    elif hasattr(model, '__dict__'):
        return model.__dict__
    else:
        return model


def to_json_list(model_list):
    json_list = []
    for model in model_list:
        json_list.append(to_json(model))
    return json_list
