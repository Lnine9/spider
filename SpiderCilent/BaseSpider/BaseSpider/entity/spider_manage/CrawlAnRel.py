from datetime import date


class CrawlAnRel:
    id: int
    spider_id: str
    crawl_history_id: str
    an_id: int
    crawl_time: date
    last_resolver: str
    exception_type: str
    exception_id: str
