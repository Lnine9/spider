
"""
关系解析器父类
"""
from abc import abstractmethod

from RelationAnalysis.entity.announcement_info import AnnouncementInfoEntity


class ResolverInterface:

    @abstractmethod
    def analysis(self, announcement_info: AnnouncementInfoEntity):
        """
        解析
        :param announcement_info:
        :return:
        """
        pass



