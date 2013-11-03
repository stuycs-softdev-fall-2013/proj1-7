from pymongo import MongoClient
from time import strftime
client = MongoClient()
posts = client.db.posts
posts.remove()

def delete(title = ""):
    if title != "":
        if posts.find({"Title":title}).count() != 0:
            posts.remove({"Title":title})

def write(title,time,post):
    if posts.find({"Title":title}).count() == 0:
        posts.insert({"Title":(title,time,post),"comments":{}})
        return True
    return False

def single(title):
    page = [x for x in posts.find({"Title":(title)},fields={"_id":False})]
    rtn = []
    rtn.append(page[0]['Title'])
    rtn.append(page[0]['comments'])
    return rtn

def getPosts():
    a=[x['Title'] for x in posts.find({},fields={"_id":False,"comments":False})]
    return a

def commentate(title,username,time,comment):
    id = [x['comments'].__len__() for x in posts.find({"Title":(title)},fields={'_id':False})]
    posts.update({'Title':(title)},{'$set':{"comments.%s"%(str(id[0])):(username,time,comment,0)}})

def upvoteComment(title,num):
    posts.update({'Title':(title)},{'$inc':{'comments.%s.3'%(str(num)):+1}})
        
if __name__ == '__main__':
    write('blog1',strftime("%X %x"),'first blog')
    write('blog2',strftime("%X %x"),'2nd blog')
    write('blog3',strftime("%X %x"),'3rd blog')
    
    print(getPosts())
    print('\n')
    print(single('blog2'))
    print('\n')
    commentate('blog2','kevin',strftime("%X %x"),'lmao')
    commentate('blog2','bob',strftime("%X %x"),'rofl')
    commentate('blog2','jason',strftime("%X %x"),'sh!t')

    print(single('blog2'))
    print('\n')
    upvoteComment('blog2',1)
    print(single('blog2'))

