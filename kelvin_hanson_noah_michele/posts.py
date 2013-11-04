from pymongo import MongoClient
from datetime import timedelta

client = MongoClient()
posts = client.KMNH.posts

def addPost(usr,title,post,date):
    posts.insert({'usr':usr, 'title':title, post:'post','datetime':datetime.datetime.now()})

def getPost(usr,title):
    if posts.find({'usr':usr,'title':title}).count != 0:
        return posts.find({'usr':usr,'title':title})['post']
    return False


def getPostTime(usr, title):
    if posts.find({'usr':usr,'title':title}).count != 0:
        return posts.find({'usr':usr,'title':title})['datetime']
    return False
                     
