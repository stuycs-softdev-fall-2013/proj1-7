from pymongo import MongoClient
from datetime import timedelta

client = MongoClient()
db = client.KMNH
users = db.users
posts = db.posts
comments = db.comments

def addComment(usr,post_id,comment,timestamp):
    if usr == None:
        usr = "guest"        
    if(post_id==None or comment==None):
        return False
    comments.insert({'usr':usr,'post_id':post_id,'comment':comment,'timestamp':datetime.datetime.now()})
    

def editComment(usr,comment,newcomment):
    if comments.find({'usr':usr,'comment':comment}).count != 0 and newcomment != None:
        comments.find_one({'usr':usr,'comment':comment}).upsert({'comment':newcomment})
        return True
    return False

def removeComment(usr,comment):
    if comments.find({'usr':usr,'comment':comment}).count != 0:
        comments.remove({'usr':usr,'comment':comment},1)
        return True
    return False
                                            
if(__name__ == "__main__"):
    
    print addComment("user", 1, "Hello World")
    
                                            
