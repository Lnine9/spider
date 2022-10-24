from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.base.param_obtain import \
    ParamObtain, getmethod
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.source_datas import \
    SourceDatas
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.tools.deal_text import \
    find_one_index
from BaseSpider.tool import DealDate


class BidEndTime(ParamObtain):

    @classmethod
    @getmethod(priority=1)
    def type1(cls):
        text = SourceDatas.text
        key = ['投标截止时间', '递交截止时间', '递交的截止时间', '提交截止时间']
        while (True):
            begin = find_one_index(text, key)
            if begin < len(text) - 50:
                bid_end_time = text[begin:begin + 50]
                bid_end_time = bid_end_time.replace(' ', '').replace('\t', '').replace('\xa0', '')
                time = DealDate.get_one_connect_time(bid_end_time)
                if time:
                    return time
                text = text[begin + 50:]
            else:
                break
        return None

    @classmethod
    def check(cls, data: str):
        return True
