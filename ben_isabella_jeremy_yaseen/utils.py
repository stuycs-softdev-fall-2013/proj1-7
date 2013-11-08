#!/usr/local/bin/python
from elasticsearch import Elasticsearch
from pymongo import MongoClient
from datetime import datetime
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
    for p in results['hits']['hits']:
        p['_source']['_id'] = p['_id']
    posts = [p['_source'] for p in results['hits']['hits']]
    return posts


def clear_index():
    query = {'match_all': {}}
    es.delete_by_query('bloginator', doc_type='post', body=query)


# From stackoverflow
def pretty_date(time=False):
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time 
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff/7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff/30) + " months ago"
    return str(day_diff/365) + " years ago"


if __name__ == '__main__':
    index_task.enter(ES_REPEAT, 1, index, ())
    index_task.run()
