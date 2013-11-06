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
    order = sorted(page[0]['comments'],key=lambda x: page[0]['comments'][x][3],reverse = True)
    rtn = []
    rtn.append(page[0]['Title'])
    rtn.append(page[0]['comments'])
    rtn.append(order)
    return rtn


def getPosts():
    if posts.find({}).count() > 0:
        a=[x['Title'] for x in posts.find({},fields={"_id":False,"comments":False})]
        return sorted(a,key=lambda x:x[1],reverse=True)
    return []

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
#    commentate('blog2','bob',strftime("%X %x"),'rofl')
#    commentate('blog2','jason',strftime("%X %x"),'damn')
#    commentate('blog2','jason',strftime("%X %x"),'god')
    
    print("commented \n " )

    print(single('blog2'))
    print('\n')
    upvoteComment('blog2',0)
#    upvoteComment('blog2',2)
#    upvoteComment('blog2',2)
    print(single('blog2'))



    
