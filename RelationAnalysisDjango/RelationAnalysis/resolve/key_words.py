import os

import jieba
import jieba.analyse
from RelationAnalysisDjango.settings import BASE_DIR

# 加载用户词库
jieba.load_userdict(os.path.join(BASE_DIR, 'RelationAnalysis/resolve/dict/user_words.txt'))

# 加载语料库
# jieba.analyse.set_idf_path('./dict/idf_words.txt')

# 加载停词库
jieba.analyse.set_stop_words(os.path.join(BASE_DIR, 'RelationAnalysis/resolve/dict/stop_words.txt'))


def get_key_words(txt: str, top_keys: int, with_weight: bool):
    """
    获取关键词
    :return:
    """
    return jieba.analyse.extract_tags(txt, topK=top_keys, withWeight=with_weight, allowPOS=('n', 'nt', 'nz', 'vn'))


def add_idf():
    """
    语料库新增
    :return:
    """
    pass


def add_stop_word():
    """
    停词库新增
    :return:
    """
    pass


