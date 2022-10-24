from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.base.param_obtain import \
    ParamObtain, getmethod
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.source_datas import \
    SourceDatas
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.tools.deal_text import \
    find_line, find_one_index
from BaseSpider.tool import DealDate


class BidSaleTime(ParamObtain):

    @classmethod
    @getmethod(priority=1)
    def type1(cls):
        text = SourceDatas.text
        keys = ['获取时间']
        while (True):
            line = find_line(text, keys)
            begin = find_one_index(line, keys)
            if begin < len(text) - 50:
                string = line[begin:begin + 50]
                times = DealDate.get_connect_time(string)
                if len(times) >= 2:
                    content = {}
                    content['bid_sale_op_time'] = times[0]
                    content['bid_sale_en_time'] = times[1]
                    return content
                text = text[begin + 50:]
            else:
                break
        return None

    @classmethod
    @getmethod(priority=2)
    def type2(cls):
        text = SourceDatas.text
        keys = ['投标人', '于', '至', '在', '招标文件']
        line = find_line(text, keys)
        string = line[find_one_index(line, keys):]
        times = DealDate.get_connect_time(string)
        if len(times) >= 2:
            content = {}
            content['bid_sale_op_time'] = times[0]
            content['bid_sale_en_time'] = times[1]
            return content

    @getmethod(priority=3)
    def type3(cls):
        text = SourceDatas.text
        keys = ['有意参加投标', '于', '至', '在', '招标文件']
        line = find_line(text, keys)
        string = line[find_one_index(line, ['有意参加投标']):]
        times = DealDate.get_connect_time(string)
        if len(times) >= 2:
            content = {}
            content['bid_sale_op_time'] = times[0]
            content['bid_sale_en_time'] = times[1]
            return content

    @classmethod
    def check(cls, data: str):
        if data:
            return True
        return False

    def schedule(self):

        pass
