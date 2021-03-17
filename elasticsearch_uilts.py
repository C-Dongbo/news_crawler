from elasticsearch import Elasticsearch, helpers
import datetime



class ES_utils():
    def __init__(self, ip_host):
        super()
        self.es = Elasticsearch(ip_host + ':9200', http_auth=("elastic","123456"))  # python에서 localhost안먹힘, host를 특정해야함

        
    def drop_index(self, index_name):
        self.es.indices.delete(index = index_name, ignore=[400,404])


    def delete_doc(self, index_name, query):
        self.es.delete_by_query(index = index_name, doc_type="_doc", body = query)

    def search(self, index_name, query):
        index = index_name
        body = {"query": {"match": {'title':query}}
        results = self.es.search(index=index, body=body)
        return results

    def insert_data(self, index_name, doc_list):
        for doc in doc_list:
            if self.contains_doc(doc['_source']['title']):
                self.es.index(index = index_name, body = doc)

    def insert_bulk_data(self, index_name, doc_list):
        index=index_name
        helpers.bulk(self.es, doc_list)

    def contains_doc(self, index_name, title):
        results = self.search(index_name, title)
        for result in results['hits']['hits']:
            if result['title'] == title:
                return True
        return False

    def get_doc_count(self, index_name):
        counts = self.es.count(index = index_name)
    