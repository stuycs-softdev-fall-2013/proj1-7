import pymongo from MongoClient

client = MongoClient();
db = client.KMNH
users = db.users
posts = db.posts
comments = db.comments

def addComment(usr="guest",post_id,comment):
    if(post_id==None or comment==None):
        return False
    comments.insert({'usr':usr,'post_id':post_id,'comment':comment})
    

def editComment(comment,newcomment):
    if comments.find({'comment':comment}).count != 0 and newcomment != None:
        comments.find_one({'comment':comment}).upsert({'comment':newcomment})
        return True
    return False

                                            

                                            
