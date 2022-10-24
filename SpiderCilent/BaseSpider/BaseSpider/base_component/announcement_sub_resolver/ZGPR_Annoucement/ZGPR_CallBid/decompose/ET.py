from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.base.param_obtain import \
    ParamObtain, getmethod
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.source_datas import \
    SourceDatas
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.tools.deal_text import \
    find_one_index, splitString


class ET(ParamObtain):

    @classmethod
    @getmethod(priority=1)
    def type1(cls):
        text = SourceDatas.text
        ET_keys = ['计划工期：', '工期要求：', '计划开竣工日期：', '工期目标：']
        end_strs = ['\n', ';', '。', '；', '！', '!']
        et = text[find_one_index(text, ET_keys):]  # 截取到开始
        proj_place = et[:find_one_index(et, end_strs)]  # 截取到结束
        if proj_place:  # 去除key
            return splitString(proj_place)[1].replace(' ', '').replace('\xa0', '').replace('\t', '')
        else:  # 切割标题
            return None

    @classmethod
    def check(cls, data: str):
        return True
