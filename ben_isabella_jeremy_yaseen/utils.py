#!/usr/local/bin/python
from elasticsearch import Elasticsearch
from pymongo import MongoClient
from settings import DB_NAME, ES_REPEAT
import sched, time

es = Elasticsearch()
cli = MongoClient()
db = cli[DB_NAME]
index_task = sched.scheduler(time.time, time.sleep)
if not es.indices.exists('bloginator'):
    es.indices.create('bloginator')


def index():
    for cursor in db.posts.find():
        p = {}
        for key in cursor:
            if key != '_id':
                p[key] = cursor[key]
        es.index(index='bloginator', doc_type='post', id=cursor['_id'], body=p)
    index_task.enter(ES_REPEAT, 1, index, ())


def search(keyword):
    query = {'query': {'match': {'_all': keyword}}}
    results = es.search(index='bloginator', doc_type='post', body=query)
    posts = [p['_source'] for p in results['hits']['hits']]
    return posts


def clear_index():
    query = {'match_all': {}}
    es.delete_by_query('bloginator', doc_type='post', body=query)


if __name__ == '__main__':
    index_task.enter(ES_REPEAT, 1, index, ())
    index_task.run()
