from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

connection = MongoClient()
db = connection.database

def add(eyeD, lines, author, title):
    lineId = db.line.insert({'author':author, 'text':lines, 'title':title, 'timestamp':datetime.datetime.now()})
    text = [s for s in db.story.find({'_id':ObjectId(eyeD)}, fields = {'text':True})][0]['text']
    text.append(lineId)
    db.story.update({'_id':ObjectId(eyeD)}, {'$set':{'text': text}})

def getLine(eyeD):
    line = [s for s in db.line.find({'_id':eyeD}, fields={'_id':False, 'text':True})]
    return line[0]['text'];

def getStories(order):
    stories = [s for s in db.story.find()]
    for s in stories:
        s['texts'] = ""
        i = 0
        while (i < len(s[u'text'])):
            s['texts'] = s['texts'] + getLine(s[u'text'][i]) + "\n"
            i = i + 1
    return stories

def getStory(eyeD):
    story = [s for s in db.story.find({'_id':ObjectId(eyeD)})]
    story = story[0]
    i = 0
    story['texts'] = ""
    while i < len(story[u'text']):
        story['texts'] = story['texts'] + getLine(story[u'text'][i]) + "\n"
        i = i + 1
    return story

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
        owned.append(story)
    lines = info['lines']
    if lines == None:
        lines = [line]
    else:
        lines.append(line)
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
