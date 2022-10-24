# -*- coding: utf-8 -*-
import re


def search_with_start_and_end(lists, start, end=None):
    """
    从字符串列表中查找以start开始end结束的字符串
    :param lists:
    :param start:
    :param end:
    :return:
    """
    if end is None:
        end = ['\n', '\r', '。']
    for content in lists:
        flag = True
        for search_str in start:
            if search_str not in content:
                flag = False
                break
        if flag:
            string = get_one_point_str(content, start)
            re_p = re.compile('|'.join(end))
            all = re_p.split(string)
            string = all[0]
            return string
    return ''


def get_one_point_str(string, lists, index=0):
    """
    从字符串中提取仅含一个关键词的子串
    :param string:
    :param lists:
    :param index: 偏移量，暂未实现
    :return:
    """
    for i in lists:
        if i in string:
            string = string[string.find(i):]
    return string


def search_in_list(lists, search_list: list):
    """
    从字符串列表中查询一个存在关键词的字符串
    :param lists:
    :param search_list:
    :return:
    """
    for content in lists:
        for search_str in search_list:
            if search_str in content:
                return content
    return ''


def search_index(lists, string):
    """
    查询字符串所在位置
    :param lists:
    :param string:
    :return:
    """
    for index in range(len(lists)):
        if string in lists[index]:
            return index


def deleteKeyWords(string, keys):
    """
    删除关键字
    当前未实现、仅以冒号分割
    :param string:
    :param keys:
    :return:
    """
    if ':' in string:
        return string[string.find(":") + 1:]
    if '：' in string:
        return string[string.find("：") + 1:]


def getListIndex(string_list, lists):
    """
    查询字符串存在的所有位置
    :param lists:
    :param string:
    :return:
    """
    count = []
    for string in string_list:
        for i, v in enumerate(lists):
            if string in v:
                count.append(i)
    return count


def removeKong(string):
    """
    删除空字符
    :param string:
    :return:
    """
    return string.replace('\n', '').replace('\t', '').replace('\xa0', '').replace('\r', '').replace(' ', '')


def splitString(string: str):
    """
    冒号分割字符串
    :param string:
    :return:
    """
    return re.split(r'[:：]', string)


def first_end(string: str):
    # 清理无效开始字符
    string = clear_start(string)

    lists = splitString(string)
    if len(lists) == 1:
        return string
    else:
        string = lists[0]
    return clear_end(string)


def clear_start(string: str):
    start = re.findall(r'^[ ,./;_`~!#&* ，。？?；：:]+', string)
    if start:
        string = string[len(start):]
    return string


def clear_end(string: str):
    find_list = re.split('[ 。;；\t\n]', string)
    return find_list[0]


# 结尾无用标点符号
punctuation = [',', '.', '?', ';', '\\', '!', '，', '。', '/', '；', '、', '-']


def delete_unuseful(string: str):
    if not string:
        return ''
    unuseful = ['\n', '\r', '\t', '\xa0', ' ']
    for u in unuseful:
        string = string.replace(u, '')
    return string[:-1] if len(string) != 0 and string[-1] in punctuation else string


# 删除字符串中的中文字符
def delete_chinese_char(str):
    match = re.compile(u'[\u4e00-\u9fa5]')
    return match.sub('', str)


# 生成xpath的条件内容
def get_contains_str(names):
    string = ''
    for name in names:
        string += 'contains(.,"{name}")'.format(name=name)
        if name != names[-1]:
            string += ' or '
    return string
