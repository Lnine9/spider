from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.base.param_obtain import \
    ParamObtain, getmethod
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.source_datas import \
    SourceDatas
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.tools.deal_text import \
    find_one_index, splitString


class BidSaleM(ParamObtain):

    @classmethod
    @getmethod(priority=1)
    def type1(cls):
        text = SourceDatas.text
        keys = ['文件获取方式：']
        end_strs = ['\n', ';', '。', '；', '！', '!']
        bid_sale_m = text[find_one_index(text, keys):]  # 截取到开始
        bid_sale_m = bid_sale_m[:find_one_index(bid_sale_m, end_strs)]  # 截取到结束
        if bid_sale_m:  # 去除key
            return splitString(bid_sale_m)[1].replace(' ', '').replace('\xa0', '').replace('\t', '')
        else:  # 切割标题
            return None

    @classmethod
    def check(cls, data: str):
        return True
