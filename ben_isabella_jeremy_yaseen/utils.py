from elasticsearch import Elasticsearch
from pymongo import MongoClient
from settings import DB_NAME


es = Elasticsearch()
cli = MongoClient()
db = cli[DB_NAME]
if not es.indices.exists('bloginator'):
    es.indices.create('bloginator')

def run():
    for cursor in db.posts.find():
        p = {}
        for key in cursor:
            if key != '_id':
                p[key] = cursor[key]
        es.index(index='bloginator', doc_type='post', id=cursor['_id'], body=p)


def search(keyword):
    query = {'query': {'match': {'_all': keyword}}}
    results = es.search(index='bloginator', doc_type='post', body=query)
    posts = [p['_source'] for p in results['hits']['hits']]
    return posts
