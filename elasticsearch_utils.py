from elasticsearch import Elasticsearch, helpers
import datetime



class ES_utils():
    def __init__(self, ip_host):
        super()
        self.es = Elasticsearch(ip_host + ':9200', http_auth=("elastic","123456"))  # python에서 localhost안먹힘, host를 특정해야함
        
    def is_exists_index(self, index_name):
        return self.es.indices.exists(index)

    def make_index(self, index_name):
        self.es.indices.create(index_name)

    def drop_index(self, index_name):
        self.es.indices.delete(index = index_name, ignore=[400,404])


    def delete_doc(self, index_name, query):
        self.es.delete_by_query(index = index_name, doc_type="_doc", body = query)

    def search(self, index_name, query):
        index = index_name
        body = {"query": {"match": {'title':query}}}
        results = self.es.search(index=index, body=body)
        return results

    def insert_data(self, index_name, doc_list):
        for doc in doc_list:
            if not self.contains_doc(index_name, doc['_source']['title']):
                print(doc)
                self.es.index(index = index_name, body = doc['_source'])



    def insert_bulk_data(self, index_name, doc_list):
        index=index_name
        helpers.bulk(self.es, doc_list)

    def contains_doc(self, index_name, title):
        results = self.search(index_name, title)
        for result in results['hits']['hits']:
            if result['_source']['title'] == title: ## 문장 유사도 필요 할듯
                return True
        return False

    def get_doc_count(self, index_name):
        counts = self.es.count(index = index_name)
    