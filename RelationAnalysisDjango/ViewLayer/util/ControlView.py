import re

from django.http import HttpResponse, JsonResponse
from django.http.response import HttpResponseBase
from django.shortcuts import render
from django.template.response import TemplateResponse

from ViewLayer import router
from RelationAnalysisDjango.tools.logger import logger


class ControlView:
    router = router

    def __init__(self):
        self.response = None
        self.request = None
        self.url = None

    @classmethod
    def as_view(cls, request, url):
        logger.debug(f"访问接口：{str(url)}")
        response = cls.filter(request, url)
        return cls.to_response(request, response) if response is not None else HttpResponse('访问失败，请求无响应', status=401)

    @classmethod
    def filter(cls, request, url):
        if '0' == '1':  # todo 校验权限
            logger.warning("权限错误，访问失败")
            return HttpResponse('访问拒绝', status=401)
        try:
            return cls.addressing(request, url)
        except Exception as e:
            logger.error(f"接口异常：{str(e.args)}", exc_info=True)
            return HttpResponse('访问拒绝', status=500)

    @classmethod
    def addressing(cls, request, url):
        urls = re.split('/', url)
        router = cls.router.urlpatterns
        if urls[-1] == '':
            urls = urls[:-1]
        if urls.count(''):
            logger.warning(f"页面未找到: {url}")
            return cls.deal_error(request, 404)

        for u in urls:
            router = router.get(u)
            if not router:
                logger.warning(f"页面未找到: {url}")
                return cls.deal_error(request, 404)

        if router:
            params = cls.get_params(request)
            if isinstance(router, dict):
                if '/' in router:
                    if router.get('/').__code__.co_argcount != 0:
                        return router.get('/')(params)
                    else:
                        return router.get('/')()
                else:
                    logger.warning(f"页面未找到: {url}")
                    return cls.deal_error(request, 404)
            else:
                if router.__code__.co_argcount != 0:
                    return router(params)
                else:
                    return router()

    @classmethod
    def to_response(cls, request, data):
        if isinstance(data, dict) and data.get('template', None):
            return render(request, data.get('template'), data.get('data'))
        elif isinstance(data, str):
            return HttpResponse(data)
        elif not isinstance(data, HttpResponseBase):
            return JsonResponse(data)
        else:
            return data

    @classmethod
    def get_params(cls, request):
        if request.method == 'POST':
            data = dict(request.POST.items())
        elif request.method == 'GET':
            data = dict(request.GET.items())
        else:
            data = {}
        return data

    @classmethod
    def deal_error(cls, request, status):
        return TemplateResponse(request, f'errors/page_{status}.html')
