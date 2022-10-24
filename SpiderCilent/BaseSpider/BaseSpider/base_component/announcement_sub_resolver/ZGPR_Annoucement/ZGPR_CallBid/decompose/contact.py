from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.base.param_obtain import \
    ParamObtain, getmethod
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.source_datas import \
    SourceDatas
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.tools.deal_text import \
    find_one_index, splitString


class Contact(ParamObtain):

    @classmethod
    @getmethod(priority=1)
    def type1(cls):
        content = {'proj_unit': None, 'proj_unit_address': None, 'proj_rel_p': None, 'proj_rel_m': None,
                   'agent_unit': None, 'agent_unit_p': None, 'agent_unit_m': None, 'agent_unit_address': None}
        text = SourceDatas.text
        begin = find_one_index(text, ['联系方法', '联系方式'])
        new_text = text[begin:]

        proj_unit_keys = ['项目单位：', '招标人：', '委托单位：', '招 标 人：', '建设单位：', '招标单位：']
        end_strs = ['\n', ';', '。', '；', '！', '!', '\t', '\n', '\xa0\xa0', '    ']
        proj_unit_begin = find_one_index(new_text, proj_unit_keys)
        content['proj_unit'] = new_text[proj_unit_begin:]  # 截取到开始
        content['proj_unit'] = content['proj_unit'][:find_one_index(content['proj_unit'], end_strs)]  # 截取到结束
        if content['proj_unit']:  # 去除key
            content['proj_unit'] = splitString(content['proj_unit'])[1].replace(' ', '').replace('\xa0', '').replace(
                '\t', '')

        agent_unit_keys = ['代理机构：']
        agent_unit_begin = find_one_index(new_text, agent_unit_keys)
        content['agent_unit'] = new_text[agent_unit_begin:]  # 截取到开始
        content['agent_unit'] = content['agent_unit'][:find_one_index(content['agent_unit'], end_strs)]  # 截取到结束
        if content['agent_unit']:  # 去除key
            content['agent_unit'] = splitString(content['agent_unit'])[1].replace(' ', '').replace('\xa0', '').replace(
                '\t', '')
        proj_unit_text = new_text[proj_unit_begin:]
        agent_unit_text = new_text[agent_unit_begin:]

        # proj_unit

        proj_unit_address_keys = ['地址：']
        content['proj_unit_address'] = proj_unit_text[find_one_index(proj_unit_text, proj_unit_address_keys):]  # 截取到开始
        content['proj_unit_address'] = content['proj_unit_address'][
                                       :find_one_index(content['proj_unit_address'], end_strs)]  # 截取到结束
        if content['proj_unit_address']:  # 去除key
            content['proj_unit_address'] = splitString(content['proj_unit_address'])[1].replace(' ', '').replace('\xa0',
                                                                                                                 '').replace(
                '\t', '')

        proj_unit_keys = ['联系人：', '经办人：']
        content['proj_rel_p'] = proj_unit_text[find_one_index(proj_unit_text, proj_unit_keys):]  # 截取到开始
        content['proj_rel_p'] = content['proj_rel_p'][:find_one_index(content['proj_rel_p'], end_strs)]  # 截取到结束
        if content['proj_rel_p']:  # 去除key
            content['proj_rel_p'] = splitString(content['proj_rel_p'])[1].replace(' ', '').replace('\xa0', '').replace(
                '\t', '')

        proj_unit_keys = ['电话：']
        content['proj_rel_m'] = proj_unit_text[find_one_index(proj_unit_text, proj_unit_keys):]  # 截取到开始
        content['proj_rel_m'] = content['proj_rel_m'][:find_one_index(content['proj_rel_m'], end_strs)]  # 截取到结束
        if content['proj_rel_m']:  # 去除key
            content['proj_rel_m'] = splitString(content['proj_rel_m'])[1].replace(' ', '').replace('\xa0', '').replace(
                '\t', '')

        # agent_unit

        proj_unit_keys = ['地址：']
        content['agent_unit_address'] = agent_unit_text[find_one_index(agent_unit_text, proj_unit_keys):]  # 截取到开始
        content['agent_unit_address'] = content['agent_unit_address'][
                                        :find_one_index(content['agent_unit_address'], end_strs)]  # 截取到结束
        if content['agent_unit_address']:  # 去除key
            content['agent_unit_address'] = splitString(content['agent_unit_address'])[1].replace(' ', '').replace(
                '\xa0', '').replace('\t', '')

        proj_unit_keys = ['联系人：']
        content['agent_unit_p'] = agent_unit_text[find_one_index(agent_unit_text, proj_unit_keys):]  # 截取到开始
        content['agent_unit_p'] = content['agent_unit_p'][:find_one_index(content['agent_unit_p'], end_strs)]  # 截取到结束
        if content['agent_unit_p']:  # 去除key
            content['agent_unit_p'] = splitString(content['agent_unit_p'])[1].replace(' ', '').replace('\xa0',
                                                                                                       '').replace('\t',
                                                                                                                   '')

        proj_unit_keys = ['电话：']
        content['agent_unit_m'] = agent_unit_text[find_one_index(agent_unit_text, proj_unit_keys):]  # 截取到开始
        content['agent_unit_m'] = content['agent_unit_m'][:find_one_index(content['agent_unit_m'], end_strs)]  # 截取到结束
        if content['agent_unit_m']:  # 去除key
            content['agent_unit_m'] = splitString(content['agent_unit_m'])[1] \
                .replace(' ', '').replace('\xa0', '').replace('\t', '')
        return content

    @classmethod
    def check(cls, data: dict):
        return True
