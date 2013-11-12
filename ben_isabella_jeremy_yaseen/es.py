#!/usr/local/bin/python
from elasticsearch import Elasticsearch
from pymongo import MongoClient
from bson import ObjectId
from models import Post
from settings import ES_REPEAT
import sched, time

es = Elasticsearch()
cli = MongoClient()
posts = Post()
index_task = sched.scheduler(time.time, time.sleep)
if not es.indices.exists('bloginator'):
    es.indices.create('bloginator')


def index():
    ids = []
    for p in posts.find():
	ids.append(p.get_id())
	p._obj.pop('_id', None)
        es.index(index='bloginator', doc_type='post', id=p._id, body=p._obj)

    query = {'query': {'match_all': {}}}
    results = es.search(index='bloginator', doc_type='post', body=query)
    for p in results['hits']['hits']:
	if ObjectId(p['_id']) not in ids:
	    es.delete('bloginator', doc_type='post', id=p['_id'])
    index_task.enter(ES_REPEAT, 1, index, ())


def search(keyword):
    query = {'query': {'fuzzy': {'_all': keyword}}}
    results = es.search(index='bloginator', doc_type='post', body=query)
    for p in results['hits']['hits']:
        p['_source']['_id'] = p['_id']
    posts = [p['_source'] for p in results['hits']['hits']]
    return posts


def clear_index():
    query = {'query': {'match_all': {}}}
    es.delete_by_query('bloginator', doc_type='post', body=query)


if __name__ == '__main__':
    index_task.enter(ES_REPEAT, 1, index, ())
    index_task.run()
