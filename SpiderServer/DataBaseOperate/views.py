import json

from django.http import JsonResponse, HttpResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
import traceback

from DataBaseOperate.data_operate.announcement.call_bid_engineering import CallBidEngineering
from DataBaseOperate.data_operate.announcement.call_bid_government import CallBidGovernment
from DataBaseOperate.data_operate.announcement.failure_bid_government import FailureBidGovernment
from DataBaseOperate.data_operate.announcement.modify_bid_government import ModifyBidGovernment
from DataBaseOperate.data_operate.announcement.results_bid_engineering import ResultsBidEngineering
from DataBaseOperate.data_operate.announcement.win_bid_government import WinBidGovernment
from DataBaseOperate.data_operate.reflect_db_operate import BatchOperaSm
from DataBaseOperate.data_operate.reflect_db_operate.GainAnnObject import randomId
from DataBaseOperate.data_operate.reflect_db_operate.batch_operate import query_operate, deal_operate, execute_sql
from DataBaseOperate.data_operate.reflect_db_operate.create_operate_dict import OperateAnnType
from DataBaseOperate.data_operate.spider_manage import spider_await_status, spider_model, spider_await, crawl_history, spider_list, \
    resolver, sub_component, spider_initialize
from DataBaseOperate.data_operate.spider_manage import Client
from DataBaseOperate.data_operate.spider_manage.crawl_history import CrawlHistory, query_latesturl
from DataBaseOperate.data_operate.spider_manage.crawl_html import CrawlHtml
from DataBaseOperate.data_operate.spider_manage.distributed_group import DistributedGroup
from DataBaseOperate.data_operate.spider_manage.reslove_data_rel import ResloveDataRel
from DataBaseOperate.data_operate.spider_manage.spider_await_status import SpiderAwaitStatus
from DataBaseOperate.setting import spid_engine
from DataBaseOperate.tools.ClassReflection import obj2Dict, dictionary_assignment
from DataBaseOperate.tools.dbobj_json import to_json


def database_operate(request):
    """
    数据库操作
    """
    try:
        data = {}
        if request.POST:
            data = json.loads(request.POST.get("data"))
        elif request.GET:
            data = json.loads(request.GET.get("data"))
        print(data)  # todo write to log
        operate = data.get('operate')
        if operate == 'query':
            back = query_operate({'class_type': data['class_type'], 'class_name': data['class_name']},
                                 data['query_info'])
        elif operate == 'executeSql':
            back = execute_sql(data['class_type'], data['sql'])
        else:
            back = deal_operate(data['items'])
        back = json.dumps(back, default=lambda x: to_json(x))
        return HttpResponse(back)
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(status=500, content=str(e.args))


def write_sm_to_db(rel):
    rel['class_type'] = 'db.sm'
    BatchOperaSm.addDictToSm(rel)


def spider_model_query(request):
    model = spider_model.query(request.POST.get('spider_id'))[0]
    return JsonResponse({'spider': obj2Dict(model)})


def spider_init_query(request):
    spider_message = spider_initialize.query(request.POST.get('spider_id'))[0]
    return JsonResponse(obj2Dict(spider_message))


def query_latest_url(request):
    return JsonResponse({'latest_url': query_latesturl(request.POST.get('spider_id'))})


def spider_await_query(request):
    return JsonResponse(obj2Dict(spider_await.query(request.POST.get('spider_id'))))


def spider_await_status_query(request):
    return JsonResponse(obj2Dict(spider_await_status.query(request.POST.get('spider_id'))))


def sas_update_status(request):
    spider_await_status.update_status(request.POST.get('spider_id'), request.POST.get('status'))
    return JsonResponse({'code': '200'})


def sas_update_latest_url(request):
    spider_await_status.update_latest_url(request.POST.get('spider_id'), request.POST.get('latest_url'))
    return JsonResponse({'code': '200'})


def sas_update_crawled_section_num(request):
    spider_await_status.update_crawled_section_num(request.POST.get('spider_id'),
                                                   request.POST.get('crawled_section_num'))
    return JsonResponse({'code': '200'})


def sas_update_aim_number(request):
    spider_await_status.update_aim_number(request.POST.get('spider_id'), request.POST.get('aim_num'))
    return JsonResponse({'code': '200'})


def sas_update(request):
    spider_id = request.POST.get('spider_id')
    crawled_section_num = request.POST.get('crawled_section_num')
    crawled_announce_num = request.POST.get('crawled_announce_num')
    complete_rate = request.POST.get('complete_rate')
    cur_offset = request.POST.get('cur_offset')
    crawl_history_id = request.POST.get('crawl_history_id')
    total_section = request.POST.get('total_section')
    spider_await_status.update(spider_id, crawled_section_num, crawled_announce_num, complete_rate, cur_offset,
                               crawl_history_id, total_section)
    return JsonResponse({'code': '200'})

def update_complete_rate(request):
    spider_id = request.POST.get('spider_id')
    complete_rate = request.POST.get('complete_rate')
    spider_await_status.update_complete_rate(spider_id, complete_rate)
    return JsonResponse({'code': '200'})


def chtml_update_section(request):
    CrawlHtml.updates(request.POST.get('spider_id'), request.POST.get('section_num'))
    return JsonResponse({'code': '200'})


def chtml_update_section_neg(request):
    CrawlHtml.update_section(request.POST.get('response_id'), request.POST.get('section'))
    return JsonResponse({'code': '200'})


def chis_id(request):
    return JsonResponse({'history_id': randomId()})


def chis_add(request):
    data = json.loads(request.POST.get("data"))
    Session = sessionmaker(bind=spid_engine)
    session = Session()
    item = CrawlHistory()
    dictionary_assignment(item, data)
    try:
        session.add(item)
        session.commit()
    except:
        session.rollback()
    session.close()
    return JsonResponse({'code': '200'})


def chis_delete(request):
    crawl_history.delete(id=request.POST.get('history_id'))
    return JsonResponse({'code': '200'})


def chis_update(request):
    history_id = request.POST.get('history_id')
    act_crawl_num = request.POST.get('act_crawl_num')
    update_time = request.POST.get('update_time')
    result = request.POST.get('result')
    crawl_history.update(id=history_id, update_time=update_time, act_crawl_num=act_crawl_num, result=result)
    return JsonResponse({'code': '200'})


def uuid(request):
    return JsonResponse({'uuid': BatchOperaSm.UUID_SHORT()})


def add_dict_to_sm(request):
    class_type = request.POST.get('class_type')
    class_name = request.POST.get('class_name')
    m_dict = eval(request.POST.get('dict'))
    rel = {'class_type': class_type, 'class_name': class_name, 'dict': m_dict}
    try:
        write_sm_to_db(rel)
        return JsonResponse({'code': '200', 'message': 'successfully crawl an announcement'})
    except IntegrityError:
        return JsonResponse({'code': '201', 'message': 'This announcement already exists'})
    except AttributeError as abe:
        return JsonResponse({'code': '202', 'message': 'Database connection error：' + str(abe.args)})
    except Exception as e:
        return JsonResponse({'code': '203', 'message': 'Data into inventory is error：' + str(e.args)})


def query_total_num(request):
    total_num = crawl_history.query_total_num(request.POST.get('spider_id'))
    return JsonResponse({'total_num': total_num})


def spider_list_query(request):
    spider_id = request.POST.get('spider_id')
    return JsonResponse({'spider': obj2Dict(spider_list.query(spider_id)[0])})


def resolver_query(request):
    spider_id = request.POST.get('spider_id')
    m_type = request.POST.get('type')
    return JsonResponse({'resolvers': obj2Dict(resolver.query(sub_model_id=spider_id, type=m_type))})


def resolver_query_by_id(request):
    id = request.POST.get('id')
    return JsonResponse({'resolvers': obj2Dict(resolver.query(id=id))})


def resolver_update(request):
    resolver_id = request.POST.get('resolver_id')
    version_no = request.POST.get('version_no')
    resolver.update(resolver_id, version_no)
    return JsonResponse({'code': '200'})


def sub_comp_query_by_parent(request):
    par_comp_id = request.POST.get('par_comp_id')
    sub_components = sub_component.query_parent_id(parent_component_id=par_comp_id)
    return JsonResponse({'sub_components': obj2Dict(sub_components)})


def chtml_query_by_spider_id(request):
    spider_id = request.POST.get('spider_id')
    section = request.POST.get('section')
    data_list = CrawlHtml.query_BySpiderID(spider_id, section)
    return JsonResponse({'data_list': obj2Dict(data_list)})


def chtml_query_by_id(request):
    chtml_id = request.POST.get('id')
    return JsonResponse({'html': obj2Dict(CrawlHtml.query_ById(chtml_id))})


def chtml_query_section_need_delete(request):
    spider_id = request.POST.get('spider_id')
    section = request.POST.get('section')
    CrawlHtml.query_section_need_delete(spider_id, section)
    return JsonResponse({'code': '200'})


def rdr_query_object(request):
    response_id = request.POST.get('response_id')
    return JsonResponse({'rel': obj2Dict(ResloveDataRel.query_object(response_id))})


def rdr_delete_all(request):
    response_id = request.POST.get('response_id')
    ResloveDataRel.delete_all(response_id=response_id)
    return JsonResponse({'code': '200'})


def an_delete_all(request):
    switch = {'CB_G': CallBidGovernment,
              'WB_G': WinBidGovernment,
              'FB_G': FailureBidGovernment,
              'MB_G': ModifyBidGovernment,
              'CB_E': CallBidEngineering,
              'RB_E': ResultsBidEngineering
              }
    announce_id = request.POST.get('announce_id')
    cls_type = request.POST.get('cls_type')
    switch.get(cls_type).delete_all(id=announce_id)
    return JsonResponse({'code': '200'})


def add_an_to_db(request):
    try:
        an_id = OperateAnnType.add_anns(json.loads(request.POST.get('item')))
        return JsonResponse({'an_id': an_id})
    except Exception as ex:
        print(ex)
        return JsonResponse(data={}, status=500)


def dis_group(request):
    return JsonResponse(DistributedGroup.queryid(request.POST.get('group_name')))


def client_update(request):
    message = request.POST.get('message')
    ip = request.POST.get('ip') if request.POST.get('ip') else None
    status = request.POST.get('status')
    start_time = request.POST.get('start_time') if request.POST.get('start_time') else None
    Client.update(message, ip=ip, status=status, start_time=start_time)
    return JsonResponse({'code': '200'})


def  sas_update_spider_await_status(request):
    data = json.loads(request.POST.get("data"))
    Session = sessionmaker(bind=spid_engine)
    session = Session()
    item = session.query(SpiderAwaitStatus).filter(SpiderAwaitStatus.spider_id == data['spider_id']).one()
    dictionary_assignment(item, data)
    session.commit()
    session.close()
    return JsonResponse({'code': '200'})
