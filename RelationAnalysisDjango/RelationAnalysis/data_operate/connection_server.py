import json
import threading
from urllib.parse import urljoin


from RelationAnalysis.tool.RequestTool import HttpSession
from RelationAnalysis.tool.logging import logger

DJANGO_DB_SERVICE = {
    'URL': 'http://localhost:8000/databaseOperate/',
    'PARAMS': {},
}

requests = HttpSession.get_http_session()


class DataInteraction:
    __instance_lock = threading.Lock()

    @classmethod
    def data_interaction(cls, uri=None, **kwargs):
        pass

    @classmethod
    def deal_operate(cls, items, uri='update', param='data'):
        """
        通过主键对数据进行修改
        :param items:
        :param uri:
        :param param:
        :return:
        """
        info = {'uri': uri, param: {
            'operate': 'deal',
            'items': items
        }}
        return cls.data_interaction(**info)

    @classmethod
    def query(cls, class_type, class_name, query_info, uri='query', param='data'):
        """
        通过一定条件进行查询
        :param class_type:
        :param class_name:
        :param query_infor:
        :param uri:
        :param param:
        :return:
        """
        info = {'uri': uri, param: {
            'operate': 'query', 'class_type': class_type, 'class_name': class_name,
            'query_info': query_info
        }}
        return cls.data_interaction(**info)

    @classmethod
    def execute_sql(cls, class_type, sql, uri='executeSql', param='data'):
        info = {'uri': uri, param: {'operate': 'executeSql', 'class_type': class_type, 'sql': sql}}
        return cls.data_interaction(**info)

    @classmethod
    def get_query_info(cls, query_start=0, query_end=None, query_number=None, query_fields=None,
                       query_condition=None, condition_rel="and", **kwargs):
        info = {'query_start': query_start, 'query_end': query_end, 'query_number': query_number,
                'query_fields': query_fields, 'query_condition': query_condition, 'condition_rel': condition_rel}
        info.update(kwargs)
        return info

    @classmethod
    def get_deal_item(cls, class_type, class_name, operate, item):
        """
        :param class_type: db.数据库简称(ann,sm,rel)
        :param class_name: 表的类名：通常是表名驼峰式
        :param operate:('update','add','delete')
        :param item: base对象或字典且包含主键
        :return:
        """
        return {'class_type': class_type, 'class_name': class_name, 'operate': operate,
                'dict': item}

    @staticmethod
    def to_json(model):
        if hasattr(model, 'to_json'):
            return getattr(model, 'to_json')()
        elif hasattr(model, '__dict__'):
            return model.__dict__
        else:
            return str(model)

    @staticmethod
    def to_json_list(model_list):
        json_list = []
        for model in model_list:
            json_list.append(DataInteraction.to_json(model))
        return json_list


class RemoteDjangoService(DataInteraction):
    __this = {
        'ip': '127.0.0.1',
        'date': None,
    }

    @classmethod
    def data_interaction(cls, uri='query', **kwargs):
        url = urljoin(DJANGO_DB_SERVICE.get('URL'), uri)
        body = DJANGO_DB_SERVICE.get('PARAMS')
        for key, value in kwargs.items():
            body[key] = json.dumps(value, ensure_ascii=False, default=lambda x: cls.to_json(x))
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        request = requests.post(url, data=body)
        status = request.status_code
        if status == 200:
            text = request.text
            try:
                return json.loads(text)
            except:
                logger.error("数据请求失败（body: %s)" % str(body), exc_info=True)
                raise Exception("数据请求失败")
        else:
            logger.error("数据请求失败（body: %s), info=%s" % (str(body), request.text), exc_info=True)
            raise Exception("数据请求失败")


class ClassType:
    DEFAULT = 'db'
    ANNOUNCEMENT = 'db.ann'
    SPIDER_MANAGE = 'db.sm'
    RELATION_ANALYSIS = 'db.rel'


DBService = RemoteDjangoService

all([DBService])
