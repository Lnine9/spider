# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import random
import time
from collections import defaultdict

import copy
from scrapy import signals

from BaseSpider import settings


class BasespiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BasespiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.


    def __init__(self):
        self.errorcount = 0
        self.retry_http_codes = [302, 403, 400, 405]
        # 预先保留在settings中的代理IP列表
        self.proxies = settings.PROXIES
        self.proxy = None


    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if self.proxy:
            request.meta['proxy'] = self.proxy



    def process_response(self, request, response, spider):
        """当下载器完成http请求，返回响应给引擎的时候调用process_response"""

        if response.status in self.retry_http_codes:
            copyproxies = copy.deepcopy(self.proxies)  # 深度拷贝代理ip
            copyproxies.remove(self.proxy)  # 将目前使用ip从中移除
            proxy = random.choice(copyproxies)  # 随机选择一个ip
            if proxy:  # 是代理ip
                self.proxy = proxy
                request.meta['proxy'] = proxy
            else:
                self.proxy = None
                request.meta['proxy'] = ''
            self.errorcount += 1
            if self.errorcount > 5:
                logging.error('error status'+str(response.status), exc_info=True)
                spider.crawler.engine.close_spider(spider, {'istrue_end': 'false', 'status': 0, 'result': '异常状态码'+str(response.status)})
            return request
        else:
            self.errorcount = 0
            return response


    def process_exception(self, request, exception, spider):
        if isinstance(exception, TimeoutError):
            return request
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        # pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
