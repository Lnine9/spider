import logging
import os
import time
from logging.handlers import RotatingFileHandler

from RelationAnalysisDjango.settings import BASE_DIR


def get_logger():
    """
    日志配置
    :return:
    """
    logger = logging.getLogger()

    logger.setLevel(logging.INFO)
    log_rq = time.strftime('%Y%m%d', time.localtime(time.time()))
    log_path = BASE_DIR + '/logs/'
    log_file = log_path + log_rq + '.log'

    rHandler = RotatingFileHandler(log_file, maxBytes=1 * 1024 * 1024 * 1024, backupCount=5, encoding='utf8')
    rHandler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(threadName)s ~ %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    rHandler.setFormatter(formatter)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(rHandler)
    logger.addHandler(console)
    return logger


def sole_logger(logger=get_logger()):
    return logger


logger = sole_logger()
all([logger])
