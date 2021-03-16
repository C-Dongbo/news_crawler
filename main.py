import logging
import datetime
from parser import naver

keywords = ['삼성전자']


if __name__ == '__main__':
    logging.info('start')
    for keyword in keywords:
        parser = naver(keyword)
        parser.get_news_info()
