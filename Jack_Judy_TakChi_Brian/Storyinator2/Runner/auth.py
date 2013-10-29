from pymongo import MongoClient

connection = MongoClient('db.stuycs.org')
db = connection.admin
db.authenticate('softdev','softdev')
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
        db.stories.insert({'title':title, 'author':author, 'date':date})
        
def FindMine(author):
    lines=list(db.lines.find({'author':author}))
    return lines

def deletestory(title):
    if storyexists(title):
        db.stories.remove({'title':title})

def authorname(title):
    name = db.stories.find_one({'title':title})['author']
    return name

def numberlines(title):
    numlines=db.stories.find_one({'title':title})['lines']
    return numlines

