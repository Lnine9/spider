from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.base.param_obtain import \
    ParamObtain, getmethod
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.source_datas import \
    SourceDatas
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.tools.deal_text import \
    find_one_index, splitString


class ProjCode(ParamObtain):

    @classmethod
    @getmethod(priority=1)
    def type1(cls):
        text = SourceDatas.text
        proj_name_keys = ['项目编号：', '项目编号:']
        end_strs = ['\n', ';', '。', '；', '！', '!']
        proj_code = text[find_one_index(text, proj_name_keys):]  # 截取到开始
        proj_code = proj_code[:find_one_index(proj_code, end_strs)]  # 截取到结束
        if proj_code:  # 去除key
            return splitString(proj_code)[1].replace(' ', '').replace('\xa0', '').replace('\t', '')
        else:  # 切割标题
            return None

    @classmethod
    def check(cls, data: str):
        if len(data) > 50:
            return False
        return True
