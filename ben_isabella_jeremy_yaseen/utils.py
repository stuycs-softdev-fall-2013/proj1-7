from elasticsearch import Elasticsearch
from pymongo import MongoClient
from settings import DB_NAME
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
    print 'hello'
    index_task.enter(5, 1, index, ())


def search(keyword):
    query = {'query': {'match': {'_all': keyword}}}
    results = es.search(index='bloginator', doc_type='post', body=query)
    posts = [p['_source'] for p in results['hits']['hits']]
    return posts

if __name__ == '__main__':
    index_task.enter(5, 1, index, ())
    index_task.run()
