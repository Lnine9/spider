from RelationAnalysis.data_operate.announcement.agency_unit import AgencyUnit
from RelationAnalysis.data_operate.announcement.call_bid_government import CallBidGovernment
from RelationAnalysis.data_operate.announcement.call_bid_unit import CallBidUnit
from RelationAnalysis.data_operate.announcement.provide_unit import ProvideUnit
from RelationAnalysis.data_operate.announcement.win_bid_government import WinBidGovernment
from RelationAnalysis.data_operate.relation_analysis.purchase_provider import PurchaseProvider
from RelationAnalysis.data_operate.spider_manage.crawl_html import CrawlHtml
from RelationAnalysis.server.central_control import CentralControl, RelationType
from RelationAnalysis.data_operate import control as db


def schedule_task(table, an_type, set_id=None, params=None, number=100):
    """
    定时任务执行方法
    :return:
    """
    control = CentralControl()
    anns = db.get_db_announcement(table, number, control.latest_version.get(an_type, None), an_type, params)
    if anns:
        for ann in anns:
            if set_id is not None:
                set_id(ann)
            control.resolver(ann, RelationType.schedule, an_type)


def CBGtask(params=None):
    schedule_task(CallBidGovernment, "CallBidGovernment", params=params)


def WBGtask(params=None):
    schedule_task(WinBidGovernment, "WinBidGovernment", params=params)


def PPtask(params=None):
    def set_id(ann):
        ann.id = ann.Id

    schedule_task(PurchaseProvider, "PurchaseProvider", set_id=set_id, params=params)


def CBUtask(params=None):
    schedule_task(CallBidUnit, "CallBidUnit", params=params)


def PUtask(params=None):
    schedule_task(ProvideUnit, "ProvideUnit", params=params)


def AUtask(params=None):
    def set_id(ann):
        ann.id = ann.Id

    schedule_task(AgencyUnit, "AgencyUnit", set_id=set_id, params=params)


def CHtask(params=None):
    table = CrawlHtml
    an_type = 'CrawlHtml'
    control = CentralControl()
    anns = db.get_db_2020_announcement(table, 100, control.latest_version.get(an_type, None))
    if anns:
        for ann in anns:
            control.resolver(ann, RelationType.schedule, an_type)


def Alltask(*args, **kwargs):
    CBGtask()
    WBGtask()
    PPtask()
    CBUtask()
    PUtask()
    AUtask()
    CHtask()
