# sourse_url
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.base.param_obtain import \
    ParamObtain
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.source_datas import \
    SourceDatas


class SourceUrl(ParamObtain):

    @classmethod
    def get(cls):
        response = SourceDatas.response
        return response.xpath('//*[@class="p_o"]//a[@href]/@href')[0]

    @classmethod
    def check(cls, data: str):
        return True
