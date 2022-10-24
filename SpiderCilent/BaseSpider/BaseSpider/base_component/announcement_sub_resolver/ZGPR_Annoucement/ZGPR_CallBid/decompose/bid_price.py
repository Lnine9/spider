import re

from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.base.param_obtain import \
    ParamObtain, getmethod
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.source_datas import \
    SourceDatas
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.tools.deal_text import \
    find_one_index, splitString


class BidPrice(ParamObtain):

    @classmethod
    @getmethod(priority=1)
    def type1(cls):
        text = SourceDatas.text
        first = ['招标文件售价', '招标文件价格','每套售价']
        bid_price = text[find_one_index(text, first):]
        end_strs = ['\n', ';', '。', '；', '！', '!']
        bid_price = bid_price[:find_one_index(bid_price, end_strs)]  # 截取到结束
        count = re.findall('[:：]', bid_price)
        if count:
            bid_price = splitString(bid_price)[1]
        return bid_price.replace(' ', '').replace('\xa0', '').replace('\t', '')

    @classmethod
    def check(cls, data: str):
        return True
