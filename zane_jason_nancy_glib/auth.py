from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

connection = MongoClient()
db = connection.database

def add(eyeD, lines, author, title):
    lineId = db.line.insert({'author':author, 'text':lines, 'title':title, 'timestamp':datetime.datetime.now()})
    text = [s for s in db.story.find({'_id':ObjectId(eyeD)}, fields = {'text':True})][0]['text']
    db.story.update({'_id':ObjectId(eyeD)}, {'$set':{'text': text.extend[lineId]}})

def getLine(eyeD):
    line = [s for s in db.line.find({'_id':eyeD}, fields={'_id':False, 'text':True})]
    return line[0]['text'];

def getStories(order):
    stories = [s for s in db.story.find()]
    return stories

def getStory(eyeD):
    story = [s for s in db.story.find({'_id':ObjectId(eyeD)})]
    story = story[0]
    text = getLine(story[u'text'][0])
    return story[u'author'], story[u'title'], text

def getStoryID(eyeD):
    story = db.story.find_one({'_id':eyeD})
    return story

def getUserID(author):
    user = db.user.find_one({'user':author})
    return user

def create(author, title, story):
    line = db.line.insert({'author':author, 'title':title, 'text':story, 'timestamp':datetime.datetime.now()})
    story = db.story.insert({'author':author, 'title':title, 'text':[line], 'timestamp':datetime.datetime.now(), 'completed':False})
    info = [s for s in db.user.find({'user':author}, fields={'owned':True, 'lines':True})][0]
    owned = info['owned']
    if owned == None:
        owned = [story]
    else:
        owned = owned.append(story)
    lines = info['lines']
    if lines == None:
        lines = [line]
    else:
        lines = lines.append(lines) 
    db.user.update({'user':author}, {'$set': {'owned':owned, 'lines':lines}})

def register(user, pw):
    if not checkuser(user):
        db.user.insert({'user':user, 'pass':pw, 'owned':[],'contributed':[], 'lines':[]})
        return True
    else:
        return False
    
def checkuser(user):
    users = [user for user in db.user.find({'user':user},
                                            fields={'_id':False,'user':True})]
    return len(users)!=0

def changePass(user, pw, npw):
    if login(user,pw):
        db.user.update({'user':user}, {'$set': {'pass':npw}})
        return True
    else:
        return False

def login(user, pw):
    users = [user for user in db.user.find({'user':user}, 
                                           fields={'_id':False,'user':True, 'pass':True})]
    if len(users) != 0:
        return users[0]['pass'] == pw
    else:
        return False
