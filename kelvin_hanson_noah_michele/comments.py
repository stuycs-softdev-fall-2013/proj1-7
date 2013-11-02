import pymongo from MongoClient

client = MongoClient();
db = client.KMNH
users = db.users

def addComment(usr="guest",post_id,comment):
    if(post_id==None or comment==None):
        return False
    comments.insert({'usr':usr,'post_id':post_id,'comment':comment,'timestamp})
    timestamp = datetime.utc.now()                                              
                                            
