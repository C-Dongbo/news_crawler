from elasticsearch import Elasticsearch, helpers
import datetime


ip_host = 'http://192.168.9.213'

def drop_index(index_name):
    es = Elasticsearch(ip_host + ':9200', http_auth=("elastic","123456"))
    es.indices.delete(index = index_name, ignore=[400,404])


def delete_doc(index_name, query):
    es = Elasticsearch(ip_host + ':9200', http_auth=("elastic","123456"))
    es.delete_by_query(index = index_name, doc_type="_doc", body = query)

def search(index_name, query):
    es = Elasticsearch(ip_host + ':9200', http_auth=("elastic","123456"))
    index = index_name
    body = query
    res = es.search(index=index, body=body)
    return res


def insert_data(index_name, doc_list):
    es = Elasticsearch(ip_host + ':9200', http_auth=("elastic","123456")) # python에서 localhost안먹힘, host를 특정해야함
    index=index_name
    

    helpers.bulk(es, doc_list)

def insert_data2(es, index_name, doc_list):
    for doc in doc_list:
        es.index(index = index_name, body = doc)



if __name__ == '__main__':
    # drop_index("test")
    # doc1 = {

    #         "product_name" : "IPHONE 12",
    #         "c_key" : "1",
    #         "price" : 13040000,
    #         "status" : 1,
    #         "@timestamp" : datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    # }
    doc2 = {
        "_op_type": "index",
        "_index" : "test",
        "_source" :{
            "product_name" : "APPLE WATCH",
            "c_key" : "2",
            "price" : 3040000,
            "status" : 1,
            "@timestamp" : datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        }
    }

    # doc3 = {
    #     "_op_type": "index",
    #     "_index" : "test",
    #     "_source" :{
    #         "product_name" : "APPLE WATCH",
    #         "c_key" : "2",
    #         "price" : 3040000,
    #         "statusㄴ" : 1,
    #         "@timestamp" : datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    #     }
    # }


    # doc4 = {
    #     "_op_type": "index",
    #     "_index" : "test",ㄴ
    #     "_source" :{
    #         "product_name" : "IPHON 11",
    #         "c_key" : "2",
    #         "price" : 12400000,
    #         "status" : 1,
    #         "@timestamp" : datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    #     }
    # }
    es = Elasticsearch(ip_host + ':9200', http_auth=("elastic","123456"))
    doc_list = []
    # doc_list.append(doc1)
    doc_list.append(doc2)
    # doc_list.append(doc3)
    # doc_list.append(doc4)

    # insert_data(index_name="test", doc_list = doc_list)
    counts = es.count(index = "test")
    print(counts)
    results = search(index_name = "test", query = {"query": {"match": {'product_name':'IPHONE'}}})
    for result in results['hits']['hits']:
        print(result['_source'])