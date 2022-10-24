import importlib

from sqlalchemy import inspect

from RelationAnalysis.data_operate.connection_server import DBService, ClassType
from RelationAnalysis.data_operate.relation_analysis.agency_information import AgencyInformation
from RelationAnalysis.data_operate.relation_analysis.announcement_information import AnnouncementInformation
from RelationAnalysis.data_operate.relation_analysis.purchaser_information import PurchaserInformation
from RelationAnalysis.data_operate.relation_analysis.resolver_entity import ResolverEntity
from RelationAnalysis.data_operate.relation_analysis.supplier_information import SupplierInformation
from RelationAnalysis.data_operate.switch_path import switch_mysql_class_path
from RelationAnalysis.tool.class_reflection import dictionary_assignment
from RelationAnalysis.tool.letter_case_name import lower_case_name


def get_version_class(class_type):
    classpath = switch_mysql_class_path(class_type, class_name='AnRelationAnalysisVersion')
    ret, cls_name = classpath.rsplit(".", maxsplit=1)

    m = importlib.import_module(ret)
    return getattr(m, cls_name)


def get_resolvers():
    """
    查询解析器版本号
    :return:
    """
    resolver_datas = DBService.execute_sql(ClassType.RELATION_ANALYSIS,
                                           "select id,name,class_path,version_no,`order`,immediate,relation_type,table_type,pre_parser " +
                                           "from (SELECT id,name,class_path,version_no,`order`,immediate,relation_type,table_type,pre_parser FROM resolver_entity where take_effect=1 order by `order`)" +
                                           " as t GROUP BY id, table_type")
    resolvers = []
    if not resolver_datas:
        resolver_datas = []
    for resolver in resolver_datas:
        resolver_obj = ResolverEntity(*resolver)
        resolvers.append(resolver_obj)
    return resolvers


def get_db_announcement(table, number, latest_version, an_type, params=None):
    """
    获得数据库公告
    :return:
    """
    keys = inspect(table).c.keys()
    ann_datas = DBService.execute_sql(table.class_type,
                                      "select {keys} from (select * from {table} {params}) as a left join an_relation_analysis_version as b on a.id=b.an_id and b.an_type='{an_type}' where b.relation_analysis_version is null or b.relation_analysis_version not REGEXP '{latest_version}' limit {number}".format(
                                          latest_version=latest_version, number=number,
                                          table=lower_case_name(table.__name__),
                                          keys=','.join(['a.' + key for key in inspect(table).c.keys()]),
                                          an_type=table.__name__,
                                          params='where ' + params if params else '')
                                      )
    anns = []
    if ann_datas:
        for ann in ann_datas:
            ann_obj = table()
            dictionary_assignment(ann_obj, dict(zip(keys, ann)))
            anns.append(ann_obj)
    return anns


def get_db_2020_announcement(table, number, latest_version):
    """
    获得数据库公告
    :return:
    """
    keys = inspect(table).c.keys()
    ann_datas = DBService.execute_sql(table.class_type, """
SELECT
    {keys}
FROM
    spider_manage.resolve_data_rel AS d
	LEFT JOIN spider_manage.an_relation_analysis_version AS b ON d.response_id = b.an_id
	JOIN spider_manage.crawl_html AS a ON d.response_id = a.id
	JOIN an.win_bid_government AS c ON d.an_id = c.id 
WHERE
	(d.spider_id = 43 OR d.spider_id = 44)
	AND ( b.relation_analysis_version IS NULL OR b.relation_analysis_version NOT REGEXP '{latest_version}' ) 
	AND c.ancm_time >= '2020-01-01 00:00:00' 
LIMIT {number};
                """.format(latest_version=latest_version, number=number,
                           keys=','.join(['a.' + key for key in inspect(table).c.keys()])))

    anns = []
    if ann_datas:
        for ann in ann_datas:
            ann_obj = table()
            dictionary_assignment(ann_obj, dict(zip(keys, ann)))
            anns.append(ann_obj)
    return anns


def update_announcement(announcement):
    announcement.update_self()


def get_relation_analysis_version(an_id, an_type, class_type):
    version_clazz = get_version_class(class_type)
    obj = version_clazz.query_one(query_fields=['relation_analysis_version'],
                                  query_condition={'an_id': an_id, 'an_type': an_type})
    if obj:
        return obj.relation_analysis_version


def update_relation_analysis(announcement_id, relation_analysis_version, an_type, class_type, real_version=None):
    version_clazz = get_version_class(class_type)
    query = version_clazz.query_one(an_id=announcement_id)
    if query:
        if real_version is None:
            query.update_self(relation_analysis_version=relation_analysis_version)
        else:
            query.update_self(relation_analysis_version=relation_analysis_version, real_version=real_version)
    else:
        version = version_clazz()
        version.id = version_clazz.UUID_SHORT()
        version.an_id = announcement_id
        version.an_type = an_type
        version.relation_analysis_version = relation_analysis_version
        version.real_version = real_version
        version.add_self()


def get_relation_table(relation_type):
    def default():
        return

    relation_switch = {
        '代理机构解析': AgencyInformation,
        '公告解析': AnnouncementInformation,
        '采购人解析': PurchaserInformation,
        '供应商解析': SupplierInformation
    }
    return relation_switch.get(relation_type, default)
