from pymongo import MongoClient

client = MongoClient()
posts = client.KMNH.posts

def addPost(usr, post):
    posts.insert({'usr':usr,'post':post,'datetime':
