import re

from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.tools.re_tools import *


def find_one_index(text, find_str_list) -> int:
    """
    查找开始位置
    :param text:
    :param find_str_list:
    :return:
    """
    return len(re.split(change_list_to_ortype(find_str_list), text)[0])


def find_one_end_index(text, find_str_list) -> int:
    """
    查找字符串的下一个所在
    :param text:
    :param find_str_list:
    :return:
    """
    key = re.findall(change_list_to_ortype(find_str_list), text)[0]
    return text.find(key) + len(key)


def splitString(string: str):
    """
    冒号分割字符串
    :param string:
    :return:
    """
    return re.split(r'[:：]', string)


def find_line(text, find_list):
    line_list = re.split('\n', text)
    for line in line_list:
        flag = True
        for find in find_list:
            if find not in line:
                flag = False
                break

        if flag:
            return line
