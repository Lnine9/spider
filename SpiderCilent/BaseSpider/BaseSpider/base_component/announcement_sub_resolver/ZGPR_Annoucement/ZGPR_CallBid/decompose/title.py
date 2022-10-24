from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.base.param_obtain import \
    ParamObtain
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.source_datas import \
    SourceDatas


class Title(ParamObtain):

    @classmethod
    def get(cls):
        response = SourceDatas.response
        return response.xpath("//h4[@class='h4_o']//text()")[0].replace(' ', '').replace('\xa0', '').replace('\t', '')

    @classmethod
    def check(cls, data: str):
        return True
