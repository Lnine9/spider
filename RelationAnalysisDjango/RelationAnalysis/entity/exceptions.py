class IgnoreException(Exception):
    pass


class RecordException(Exception):
    name = "RecordException"


class WinBidAssociationFailureException(RecordException):
    name = "中标公告关联失败"

    def __init__(self, *args):
        self.args = args if args else ("中标公告关联失败，公告未匹配成功",)

    def __str__(self):
        return str(self.args)
