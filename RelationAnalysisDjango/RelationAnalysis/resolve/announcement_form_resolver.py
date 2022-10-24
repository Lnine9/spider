"""
代理机构解析器（新版）
"""

from lxml import etree

from RelationAnalysis.data_operate.connection_server import DBService
from RelationAnalysis.data_operate.pool_table import SMTable
from RelationAnalysis.data_operate.spider_manage.crawl_html import CrawlHtml
from RelationAnalysis.resolve.address_identification import AddressIdentification
from RelationAnalysis.resolve.getData import table_and_table, div_table, p_and_table, all_table, judge_is_need, \
    get_category_entity
from RelationAnalysis.resolve.resolver_interface import ResolverInterface
from RelationAnalysis.resolve.table_contents import obtain_td_matrix

address_identification = AddressIdentification()


class AnnouncementFormResolver(ResolverInterface):

    def analysis(self, crawHtml: CrawlHtml):
        spider_id = int(crawHtml.spider_id)
        if spider_id != 43 and spider_id != 44:
            return None

        text = etree.HTML(crawHtml.content)

        listOfCategory = []
        supplierName = []
        totalPrice = []
        # 提取信息
        for index, item in enumerate(text.xpath('//div[@class="vF_detail_content"]//table')):
            listOfCategory.append(obtain_td_matrix(item))

        category = []
        tableList = []
        tableType = len(listOfCategory)

        if tableType == 1:
            nodes = text.xpath('//div[@class="vF_detail_content"]/*')
            onlyTable = True

            # 判断是否只拿table数据
            for tag in nodes:
                if str(tag.tag) == 'p':
                    onlyTable = False

            if onlyTable:
                category = all_table(listOfCategory)
            else:
                category = p_and_table(text, listOfCategory)
        else:
            title = str(listOfCategory[0])
            titleList = []
            if '金额' in title and '中标' in title or '总价' in title or '合价' in title or '成交金额' in title:
                title_list = listOfCategory[0]
                tableList = judge_is_need(listOfCategory[1:])
                for title in title_list:
                    for col, text in enumerate(title):
                        if '供应商名称' in text:
                            supplierName = [title_list[1][col]]
                        if '金额' in text and '中标' in text or '总价' in text or '合价' in text or '成交金额' in text:
                            totalPrice = [title_list[1][col]]
                category = get_category_entity(tableList, supplierName, totalPrice)
            else:
                for message in text.xpath('//div[@class="vF_detail_content"]//text()'):
                    content = message.replace(' ', '').replace('\n', '').strip("\n\r    \xa0").replace('\t', '')
                    if '供应商名称' in content:
                        if "：" in content:
                            supplierName.append(content.split("：")[1])

                    if '金额' in content and '中标' in content or '总价' in content or '合价' in content or '成交金额' in content:
                        if "：" in content:
                            totalPrice.append(content.split("：")[1])

                    if '主要标的信息' in content:
                        break
                tableList = judge_is_need(listOfCategory)
                category = get_category_entity(tableList, supplierName, totalPrice)

        an_id = get_an_id(crawHtml.id)
        if len(an_id) == 0:
            an_id = 1
        for item in category:
            item.an_id = an_id[0][0]

        return {'add': category,
                'history': {'resolver_id': getattr(self, 'id'), 'announcement_id': crawHtml.id,
                            'relation': category}}


def get_an_id(id):
    return DBService.execute_sql(SMTable.class_type,
                                 "SELECT an_id FROM `resolve_data_rel` WHERE response_id = {id}".format(
                                     id=id)
                                 )
