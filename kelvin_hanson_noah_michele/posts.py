from pymongo import MongoClient
from datetime import timedelta

client = MongoClient()
posts = client.KMNH.posts
comments = db.comments

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

def getPosts(usr):
    if posts.find({'usr':usr,}).count != 0:
        return posts.find({'usr':usr})['post']
    return False
                     
