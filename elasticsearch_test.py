from elasticsearch import Elasticsearch, helpers
import datetime



def search(index_name, query):
    es = Elasticsearch('http://192.168.1.253:9200', http_auth=("elastic","123456"))
    index = index_name
    body = query
    res = es.search(index=index, body=body)
    return res


def insert_data(index_name, doc_list):
    es = Elasticsearch('http://192.168.1.253:9200', http_auth=("elastic","123456")) # python에서 localhost안먹힘, host를 특정해야함
    index=index_name
    
#    for doc in doc_list:
#        es.index(index=index, doc_type="_doc", body=doc)
    helpers.bulk(es, doc_list)

if __name__ == '__main__':


    doc1 = {
        "_index" : "test",
        "_source" :{
            "category" : "APPLE WATCH",
            "c_key" : "1",
            "price" : 3040000,
            "status" : 1,
            "@timestamp" : datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        }
    }
    doc2 = {
        "_index" : "test",
        "_source" :{
            "category" : "APPLE WATCH",
            "c_key" : "2",
            "price" : 3040000,
            "status" : 1,
            "@timestamp" : datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        }
    }
    doc_list = []
    doc_list.append(doc1)
    doc_list.append(doc2)

    #insert_data(index_name="test", doc_list = doc_list)
    search(index_name = "test", query = {"query": {"match_all": {}}})