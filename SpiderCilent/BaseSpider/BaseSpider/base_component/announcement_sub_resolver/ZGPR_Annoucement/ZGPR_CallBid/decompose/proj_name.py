# 项目名称
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.base.param_obtain import \
    ParamObtain, getmethod
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.source_datas import \
    SourceDatas
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.tools.deal_text import *


class ProjName(ParamObtain):

    @classmethod
    @getmethod(priority=1)
    def type1(cls):
        """
        \n项目名称：xxx\n
        :param text:
        :return:
        """
        text = SourceDatas.text
        proj_name_keys = ['项目名称：', '项目名称:', '工程名称：']
        end_strs = ['\n', ';', '。', '；', '！', '!']
        proj_name = text[find_one_index(text, proj_name_keys):]  # 截取到开始
        proj_name = proj_name[:find_one_index(proj_name, end_strs)]  # 截取到结束
        if proj_name:  # 去除key
            return splitString(proj_name)[1].replace(' ', '').replace('\xa0', '').replace('\t', '')
        else:  # 切割标题
            return None

    @classmethod
    @getmethod(priority=2)
    def type2(cls):
        """
        本招标项目xxx已由...
        :param text:
        :return:
        """
        text = SourceDatas.text
        begin = find_one_end_index(text, ["本招标项目"])
        proj_name = text[begin:]
        end = find_one_index(proj_name, ['已由'])
        proj_name = proj_name[:end]
        return proj_name.replace(' ', '').replace('\xa0', '').replace('\t', '')

    @classmethod
    @getmethod(priority=100)
    def get_from_title(cls):
        """
        从标题获取title
        :param title:
        :return:
        """
        title = SourceDatas.title
        remove_list = ['招标公告', '公告']
        for rm in remove_list:
            title = title.replace(rm, '')
        return title

    @classmethod
    def check(cls, data: str):
        if data:
            if len(data) > 200:
                return False
            return True
        return False
