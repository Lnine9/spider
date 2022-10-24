# coding: utf-8
import re
import time
import requests
from urllib import parse
from RelationAnalysis.data_operate.relation_analysis.purchase_provider import PurchaseProvider
from RelationAnalysis.data_operate.pool_table import RelTable
from RelationAnalysis.data_operate.relation_analysis.resolve_history import ResolveHistory
from RelationAnalysis.resolve.resolver_interface import ResolverInterface
from RelationAnalysis.tool.logging import logger


class MainScopeResolver(ResolverInterface):

    def __init__(self):
        self.all_item = {}

    def analysis(self, provider: PurchaseProvider):
        """
        供应商经营范围解析
        通过供应商名称从爱企查查询
        因需要休眠太过耗时，故单独写成一个解析器
        :param provider:
        :return:
        """

        # 经营范围（需要休眠太耗时，此处不解析，单独写了个解析器去解析）
        if not provider.MainScope:
            provider.MainScope = self.get_scope(provider.OrgName)
            provider.update_self()

        # 历史记录入库
        try:
            self.save_resolver_history(provider.Id, provider.Id)
        except Exception as e:
            logger.error("供应商经营范围解析信息入库异常！异常信息："+str(e))
            logger.error("异常解析入库供应商id："+str(provider.Id))
        finally:
            pass

    def save_resolver_history(self, announcement_id, relation_id):
        """
        解析历史记录入库
        :param announcement_id:
        :param relation_id:
        :return:
        """
        resolver_history = ResolveHistory()
        resolver_history.id = RelTable.UUID_SHORT()
        resolver_history.parsing_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        resolver_history.relation_type = "供应商经营范围解析"
        resolver_history.announcement_id = announcement_id
        resolver_history.relation_id = relation_id
        resolver_history.add_self()

    @staticmethod
    def get_scope(supplier_name):
        supplier_name = parse.quote(supplier_name)  # url decode编码
        url = 'https://aiqicha.baidu.com/s?q=' + supplier_name + '&t=0'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
        response = requests.get(url, headers=headers)
        time.sleep(7)
        try:
            x = re.findall('\"scope\":.*?(?=,")', response.text)
            if x:
                scope = x[0][x[0].find(':') + 1:]
                return eval('u' + scope).encode('UTF-8').decode('UTF-8')
            return ''
        except Exception as e:
            logger.error(str(e))
            return ''


