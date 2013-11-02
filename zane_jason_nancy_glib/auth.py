from pymongo import MongoClient

connection = MongoClient()
db = connection.database

def getStories():
    stories = [s for s in db.story.find()]
    return stories

def getStory(title):
    story = [s for s in db.story.find({'title':title})]
    story = story[0]
    story = story[u'story']
    return story

def getStoryID(eyeD):
    story = db.story.find_one({'_id':eyeD})
    return story

def create(author, title, story):
    db.story.insert({'author':author, 'title':title, 'story':story})

def register(user, pw):
    if not checkuser(user):
        db.login.insert({'user':user, 'pass':pw})
        return True
    else:
        return False
    
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
    if len(users) != 0:
        return users[0]['pass'] == pw
    else:
        return False
