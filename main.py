import logging
import datetime
from parser import naver
from elasticsearch_utils import ES_utils

keywords = ["삼성전자"]


if __name__ == '__main__':
    logging.info('start')
    ip_host = 'http://127.0.0.1'
    es_utils = ES_utils(ip_host)
    es_utils.drop_index("news_삼성전자")
    pre_doc_id = 0
    for keyword in keywords:
        index_name = "news_{}".format(keyword)
        if es_utils.is_exists_index:
            pre_doc_id = es_utils.get_doc_count()
        else:
            es_utils.make_index(index_name)

        
        logging.info('query : {}, pre_documents_num : {}'.format(keyword, pre_doc_id))
        parser = naver(keyword)
        parser.set_id(pre_doc_id)
        results = parser.get_news_info()
        es_utils.insert_data(index_name=index_name, doc_list = results)
        logging.info('query : {}, total_news_num : {}, cluster_news_num : {}'.format(keyword, parser.get_total_news_num(), parser.get_cluster_news_num()))
    logging.info('end')


    