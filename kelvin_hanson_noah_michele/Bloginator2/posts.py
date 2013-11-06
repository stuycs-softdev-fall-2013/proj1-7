from pymongo import MongoClient
from datetime import timedelta

client = MongoClient()
db = client.KMNH
posts = client.KMNH.posts
comments = db.comments

def addPost(user,title,post,date):
    posts.insert({'title':title, post:'post','datetime':date})

def getPost(title):
    if posts.find({'title':title}).count != 0:
        return posts.find_one({'title':title})['post']
    return False

def getPostTime(title):
    if posts.find({'title':title}).count != 0:
        return posts.find({'title':title})['datetime']
    return False

def getPosts(usr):
    if posts.find({'usr':usr,}).count != 0:
        return posts.find({'usr':usr})['post']
    return False
                     
def getPosts():
    return posts.find()
