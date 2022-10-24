from urllib.parse import parse_qs, parse_qsl, urlencode

FORM_DATA = {
    'BID_PLATFORM': '0',
    'DEAL_CITY': '0',
    'DEAL_CLASSIFY': '00',
    'DEAL_PLATFORM': '0',
    'DEAL_PROVINCE': '0',
    'DEAL_STAGE': '0000',
    'DEAL_TIME': '02',
    'DEAL_TRADE': '0',
    'PAGENUMBER': '1',
    'SOURCE_TYPE': '1',
    'TIMEBEGIN': '2022',
    'TIMEBEGIN_SHOW': '2022',
    'TIMEEND': '2022',
    'TIMEEND_SHOW': '2022',
    'isShowAll': '1'
}

print(urlencode(FORM_DATA))