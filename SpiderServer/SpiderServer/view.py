from SpiderServer.service import spider_distributed


def get_client_task(request):
    """
    获取任务接口
    :param request: 请求信息
    :return:
    """
    password = request.GET.get("password")
    return spider_distributed.get(password)