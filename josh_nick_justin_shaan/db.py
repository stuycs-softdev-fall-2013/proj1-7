

#Tables:

#Users(username TEXT, password TEXT, admin int);
    #if administrative user, admin == 1, else if normal user, admin == 0

#Posts(author TEXT, title TEXT, body TEXT, comments BLOB, date text);
    #comments are a list of integers, which are the _ids of the comments in chronological order

#Comments(author Text, body TEXT, post TEXT, date text);
    #post is the _id of corresponding point

import sqlite3;
connection = sqlite3.connect('blog.db');



#precondition: name, pwd are str. priv is int [0,1]
#postcondition:
  #returns _id of new user if successful, else returns None
  #unsuccessful if given username already exits
def adduser(name, pwd, priv):
    #if isinstance(pwd, str):
    #    pass;
    q ="select username from Users where username=%s"%(name)
    o = connection.execute(q)
    if(o != None):
        insert into Users values(name, pwd, priv)
        q = "select _id from Users where username =%s"%(name)
        return connection.execute(q)
    else:
        return None
        
#precondition: name, pwd are str
#postcondition:
  #returns True if pwd matches username
  #returns False if pwd doesn't match username
  #returns False if user with username of name DNE
def authuser(name, pwd):
    q = "select username from Users where username=%s"%(name)
    username = connection.execute(q)
    if(username == None):
        return False
    q = "select password from Users where username=%s"%(pwd)
    password = connction.execute(q)
    if(password == pwd):
        return True
    else:
        return False
    
#precondition: name is str
#postcondition:
    #returns True if user successfully removed
    #returns False if user DNE
def removeuser(name):
    q = "select username from Users where username=%s"%(name);
    usr = connection.execute(q);
    if(usr == None):
        return False;
    q = "DELETE from Users where username=%s"%(name);
    connection.execute(q);
    return True;

#precondition: usr is str
#postcondition:
    #returns True if user is an admin
    #returns False if user is not admin
    #returns False if user DNE
def isAdmin(name):
    q = "select admin from Users where username=%s"%(name);
    priv = connection.execute(q)
    if(priv == None):
        return False;
    if(priv == 1):
        return True;
    else:
        return False;


#precondition: author,title,body are str
#              date is a date thing
#postcondition:
    #returns True if post creation successful
    #returns False if user with username=author DNE;
    #returns False if post with same title already exists
def addpost(author, title, body, date):
    q = "select username from Users where username=%s"%(author);
    athr = connection.execute(q);
    if(athr == None):
        return False;
    q = "select title from Posts where title=%s"%(title);
    tt = connection.execute(q);
    if(tt == None):
        return False;
    q = "INSERT into Users VALUES(%s,%s,%s,'',%s)"%(author, title, body, date);
    connection.execute(q);
    return True;
    
#precondition: title is str
#postcondition:
    #returns False if no post with given title exists
    #returns True if remove successful
def removepost(title):
    q = "select title from Users where title=%s"%(title);
    t = connection.execute(q);
    if(t == None):
        return False;
    q = "delete from Users where title=%s"%(title);
    connection.execute(q);
    return True;;

def addcomment():
    pass

def removecomment():
    pass

def getAllTitles():
    pass
