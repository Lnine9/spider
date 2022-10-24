from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.base.param_obtain import \
    ParamObtain, getmethod
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.source_datas import \
    SourceDatas
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.tools.deal_text import \
    find_one_index, splitString


class ProjPlace(ParamObtain):

    @classmethod
    @getmethod(priority=1)
    def type1(cls):
        """
        \n项目名称：xxx\n
        :param text:
        :return:
        """
        text = SourceDatas.text
        proj_name_keys = ['项目地点：', '建设地点：', '工程地址：']
        end_strs = ['\n', ';', '。', '；', '！', '!']
        proj_place = text[find_one_index(text, proj_name_keys):]  # 截取到开始
        proj_place = proj_place[:find_one_index(proj_place, end_strs)]  # 截取到结束
        if proj_place:  # 去除key
            return splitString(proj_place)[1].replace(' ', '').replace('\xa0', '').replace('\t', '')
        else:  # 切割标题
            return None

    @classmethod
    def check(cls, data: str):
        return True
