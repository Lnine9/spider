from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.base.param_obtain import \
    ParamObtain, getmethod
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.source_datas import \
    SourceDatas


class ResourceFrom(ParamObtain):

    @classmethod
    @getmethod(priority=1)
    def get_from_xpath(cls):
        response = SourceDatas.response
        resource_form = response.xpath('//*[@class="p_o"]/*[contains(.,"信息来源")]//text()')
        if len(resource_form) > 1:
            return resource_form[1].replace(' ', '').replace('\xa0', '').replace('\t', '')
        else:
            return None

    @classmethod
    def check(cls, data: str):
        return True
