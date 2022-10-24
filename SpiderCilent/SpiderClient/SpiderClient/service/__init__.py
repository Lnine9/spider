import redis
from scrapyd_api import ScrapydAPI

m_scrapyd = ScrapydAPI('http://localhost:6688')
m_redis = redis.Redis('127.0.0.1', port=6379, db=0, password='Abc785342')

spider_jobs = {}