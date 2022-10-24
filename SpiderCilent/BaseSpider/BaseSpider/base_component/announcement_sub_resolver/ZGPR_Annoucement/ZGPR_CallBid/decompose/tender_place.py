from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.base.param_obtain import \
    ParamObtain, getmethod
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.source_datas import \
    SourceDatas
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.tools.deal_text import \
    find_one_index


class TenderPlace(ParamObtain):

    @classmethod
    @getmethod(priority=1)
    def type1(cls):
        text = SourceDatas.text
        begin_keys = ['递交投标文件', '响应文件的提交', '投标文件的递交', '文件递交']
        begin = find_one_index(text, begin_keys)
        new_text = text[begin:]
        keys = ['地点为', '地点：']
        new_text = new_text[find_one_index(new_text, keys):]
        end_strs = ['\n', ';', '。', '；', '！', '!']
        tender_place = new_text[3:find_one_index(new_text, end_strs)]  # 截取到结束
        return tender_place.replace(' ', '').replace('\xa0', '').replace('\t', '')

    @classmethod
    def check(cls, data: str):
        if data:
            return True
        return False
