from pymongo import MongoClient

connection = MongoClient()
db = connection.database
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


def storyexists(title):
    return db.stories.find_one({'storytitle':title})

def addstory(title, author, date):
    if not storyexists(title):
        db.stories.insert({'title':title, 'author':author, 'date':date, 'addedlines':0})

def savenewstory(title):
    story = db.stories.find_one({'title':title})
    story['addedlines'] = story['addedlines'] + 1
    db.stories.save(story)        
    
def addtostory(line,title):
    db.lines.insert({'line':line, 'title':title})
    increment_lines(title)

def getmine(author):
    story= [s for s in db.stories.find({}, fields={'_id':False, 'author':author})]
    return story
def getall():
    stories = [s for s in db.stories.find({}, fields={'_id':False, 'title':True, 'story':True})]
    return stories
def deletestory(title):
    if storyexists(title):
        db.stories.remove({'title':title})

def authorname(title):
    name = db.stories.find_one({'title':title})['author']
    return name

def storylines(title):
    lines=db.stories.find_one({'title':title})['lines']
    return lines
