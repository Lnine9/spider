from RelationAnalysis.data_operate.announcement.call_bid_government import CallBidGovernment
from RelationAnalysis.data_operate.announcement.failure_bid_government import FailureBidGovernment
from RelationAnalysis.data_operate.announcement.modify_bid_government import ModifyBidGovernment
from RelationAnalysis.data_operate.announcement.win_bid_government import WinBidGovernment

ann_selector = {
    'CB_G': CallBidGovernment,
    'FB_G': FailureBidGovernment,
    'MB_G': ModifyBidGovernment,
    'WB_G': WinBidGovernment
}


def default(*args, **kwargs):
    return None


def create_ann(type, item):
    """
    创建公告对象
    :param type:
    :param item:
    :return:
    """
    obj = ann_selector.get(type, default)()
    if obj:
        obj.__dict__.update(item)
    return obj
