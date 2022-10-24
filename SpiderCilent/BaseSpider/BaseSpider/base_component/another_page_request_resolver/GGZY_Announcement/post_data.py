import datetime
from enum import Enum

# GGZY_START_TIME = datetime.datetime.now().strftime('%Y') + '-01-01'
GGZY_START_TIME = '2022-03-04'
GGZY_END_TIME = datetime.datetime.now().strftime('%Y-%m-%d')
FORM_DATA = {
    'BID_PLATFORM': '0',
    'DEAL_CITY': '0',
    # 类型 01 工程建设 02 政府采购
    'DEAL_CLASSIFY': '02',
    'DEAL_PLATFORM': '0',
    'DEAL_PROVINCE': '0',
    'DEAL_STAGE': '0000',
    'DEAL_TIME': '06',
    'DEAL_TRADE': '0',
    'PAGENUMBER': '1',
    'SOURCE_TYPE': '1',
    'TIMEBEGIN': GGZY_START_TIME,
    'TIMEBEGIN_SHOW': GGZY_START_TIME,
    'TIMEEND': GGZY_END_TIME,
    'TIMEEND_SHOW': GGZY_END_TIME,
    'isShowAll': '1'
}


# 具体这个请求数据不同类型是不同的，不同类型公告变一下

class Stage(Enum):
    # 采购公告：CB_G: call_bid_government
    # 中标公告：WB_G: win_bid_government
    # 废标公告：FB_G: failure_bid_government
    # 更正公告：MB_G: modify_bid_government
    # 工程采购：CB_E: call_bid_engineering

    # 政府采购招标
    CB_G = '0201'
    # 政府采购中标
    WB_G = '0202'
    # 工程建设招标
    CB_G_GC = '0101'
    # 工程建设中标
    WB_G_GC = '0104'
