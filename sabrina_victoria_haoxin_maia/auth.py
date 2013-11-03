from pymongo import MongoClient
client = MongoClient()
users = client.db.users

def authenticate(username,pw):
    return users.find({"username":username,"pw":pw},field={"_id":False}).count() != 0

def changepw(username,pw):
    users.update({'username':username},{"%$set":{'pw':pw}},upsert=False)

def register(username,pw,pw2):
    l = [x for x in users.find({"username":username})]
    num = len([x for x in users.find()])
    if users.find({"username":username}).count() != 0:
        return 1
    elif pw != pw2:
        return 2
    elif users.find().count() == 0:
        users.insert({"username":username,"pw":pw,"ADMIN":True})
    else:
        users.insert({"username":username,"pw":pw,"ADMIN":False})
    return 0

def admin(username):
    return users.find({"username":username,"ADMIN":True}).count() != 0
