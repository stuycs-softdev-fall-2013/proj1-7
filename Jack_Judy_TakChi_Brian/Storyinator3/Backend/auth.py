from pymongo import MongoClient
from time import time

def init():
    client = MongoClient()
    db = client.proj
    return db
#login
def register(user, pw):
    if checkuser(user) == False:
        db.login.insert({'user':user, 'pass':pw})
        return True
    
def checkuser(user):
    users = [user for user in db.login.find({'user':user},
                                            fields={'_id':False,'user':True})]
    return len(users)!=0

def changePass(user, pw, npw):
    if login(user,pw):
        db.login.update({'user':user}, {'$set': {'pass':npw}})
        return True
    else:
        return False

def login(user, pw):
    users = [user for user in db.login.find({'user':user},
                                           fields={'_id':False,'user':True, 'pass':True})]
    return users[0]['pass'] == pw
############################################################################################
#story stuff
def storyexists(title):
    db=init()
    return db.stories.find_one({'storytitle':title})

def makestory(title, author, story, date):
    db=init()
    if not storyexists(title):
        db.stories.insert({'title':title, 'author':author, 'story':story, 'time':time(), })
    else:
        return "Title already exists. Please create a new title."

def addtostory(lines,title):
    db=init()
    data = [s for s in db.stories.find({'title':title},fields={'_id':False})]
    data = data[0]
    new = data['title']+lines
    db.stories.update({'title':title},{'$set':{'story':new}})


def FindMine(author):
    db=init()
    story= [s for s in db.stories.find({}, fields={'_id':False, 'author':author})]
    return story
def FindAll():
    db=init()
    stories = [s for s in db.stories.find({}, fields={'_id':False, 'title':True, 'story':True})]
    return stories
def deletestory(title):
    db=init()
    if storyexists(title):
        db.stories.remove({'title':title})
    else:
        return "There is no story under that title."

def authorname(title):
    db=init()
    data = [s for s in db.stories.find({'title':title},fields={'_id':False})]
    return data['author']

def storylines(title):
    db=init()
    lines=db.stories.find({'title':title},fields={'_id':False})
    return lines
