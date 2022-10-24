from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.base.param_obtain import \
    ParamObtain, getmethod
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.source_datas import \
    SourceDatas
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.tools.deal_text import \
    find_one_index


class BidSalePlace(ParamObtain):

    @classmethod
    @getmethod(priority=1)
    def type1(cls):
        pass

    @classmethod
    @getmethod(priority=2)
    def type2(cls):
        text = SourceDatas.text
        first_keys = ['招标文件的领取']
        new_text = text[find_one_index(text, first_keys):]
        second_keys = ['领取方式']
        new_text = new_text[find_one_index(new_text, first_keys):]
        end_strs = ['\n', ';', '。', '；', '！', '!']
        sale_place = new_text[:find_one_index(new_text, end_strs)]  # 截取到结束
        return sale_place.replace(' ', '').replace('\xa0', '').replace('\t', '')

    @classmethod
    def check(cls, data: str):
        if data:
            return True
        return False
