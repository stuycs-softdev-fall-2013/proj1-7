from pymongo import MongoClient

client = MongoClient()
posts = client.KMNH.posts

def addPost(usr,title,post,date):
    posts.insert({'usr':usr, 'title':title, post:'post','datetime':date})

def getPost(user,title):
    blog = posts.find_one({'usr':user,'title':title})
    return blog
                     
