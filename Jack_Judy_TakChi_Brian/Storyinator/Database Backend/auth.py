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

def addstory(story):
    db.login.insert({'story':story})

def followedstory(story):
    db.login.insert({'followed':story})
#!/usr/bin/python
#!flask/bin/python

#This is Jack Cahn and Alvin Leung's Project

import sqlite3
connection = sqlite3.connect('test.db')
create table logins(username  text, password text);
cursor = connection.execute(q)

#results=[]
#for line in cursor:
#    results.append(line)
results = [line for line in cursor]

print results
# for line in cursor:
#     print line[0]

# print "Second time"
# for line in cursor:
#     print line

def adduser(username,password): 
    if authenticateRegister(username): 
        return False
    else: 
        q = 'INSERT INTO logins VALUES(%(username)s,%(password)s)';
        d = {'username': username,
             'password': password}
        connection.execute(q%(d))
        return True; 

def authenticate(username,password):
    authen = """
    select logins.username where logins.username = %(username)s and logins.password = %(password)s
    """
    d = { 
        'username' : username, 
        'password' : password}
    
    cursor = connection.execute(authen%(d))
    results = [line for line in cursor]
    return results != []

def authenticateRegister(username):
    authen2 = """
    select logins.username where logins.username = %(username)s
    """
    d = {'username' : username}
    
    cursor = connection.execute(authen2%(d))
    results = [line for line in cursor]
    return results != []


