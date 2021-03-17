import logging
import datetime
from parser import naver
from elasticsearch_utils import ES_utils

keywords = ["삼성전자"]


if __name__ == '__main__':
    logging.info('start')
    ip_host = 'http://127.0.0.1'
    es_utils = ES_utils(ip_host)
    logging.info()
    for keyword in keywords:
        pre_doc_cnt = es_utils.get_doc_count("news_"+keyword)
        logging.info('query : {}, pre_documents_num : {}'.format(keyword, pre_doc_cnt))
        parser = naver(keyword)
        results = parser.get_news_info()
        es_utils.insert_data(index_name="news_"+keyword, doc_list = results)
        logging.info('query : {}, total_news_num : {}, cluster_news_num : {}'.format(keyword, parser.get_total_news_num(), parser.get_cluster_news_num()))
    logging.info('end')


    