from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.base.param_obtain import \
    ParamObtain
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.source_datas import \
    SourceDatas
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.tools.deal_text import \
    find_one_index, splitString


class Region(ParamObtain):

    @classmethod
    def type1(cls):
        text = SourceDatas.text
        keys = ['行政区域：']
        end_strs = ['\n', ';', '。', '；', '！', '!']
        region = text[find_one_index(text, keys):]  # 截取到开始
        proj_place = region[:find_one_index(region, end_strs)]  # 截取到结束
        if proj_place:  # 去除key
            return splitString(proj_place)[1].replace(' ', '').replace('\xa0', '').replace('\t', '')
        else:  # 切割标题
            return None

    @classmethod
    def check(cls, data: str):
        return True
