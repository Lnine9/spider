from BaseSpider.data_operate.spider_manage import sub_component,resolver
from BaseSpider.data_operate.spider_manage.crawl_html import CrawlHtml
from BaseSpider.data_operate.spider_manage.reslove_data_rel import ResloveDataRel


class Text:
    spider_id = 7

    def parse_response_data(self, id):
        result = self.get_response_data_byid(id)  # 通过id得到response数据
        response = result.content
        if self.judge_join_taskqueue(result):
            pass  # 加入队列
    def judge_join_taskqueue(self,result):

        rel_object = ResloveDataRel.query_object(result.id)
        if not rel_object:  # 关联表是否存在相关信息
            return True
        elif rel_object[0].version_no == self.get_component_new_version_no(priority=rel_object[0].priority):  #关联信息版本号表是否最新
            return True
        return False

    def get_component_new_version_no(self,priority):
        READ_HM_TPYE = 'READ_HM'
        new_version_no = ''
        fa_component_id = resolver.query(sub_model_id=self.spider_id, type=READ_HM_TPYE, priority=priority)[0].id
        result = sub_component.query_parent_id(parent_component_id=fa_component_id)
        for item in result:
            new_version_no += item.version_no
        return new_version_no
        """
    根据id查询response数据
    """

    def get_response_data_byid(self,id):
        result = CrawlHtml.query_ById(id=id)
        return result
Text().parse_response_data(id='98710625307328641')
