

#Tables:

#Users(username TEXT, password TEXT, admin int);
    #if administrative user, admin == 1, else if normal user, admin == 0

#Posts(author TEXT, title TEXT, body TEXT, comments TEXT, date text);
    #comments are the _id's of the comments in chronological order
      #seperated by commas e.g. "sjw43jeid,2klsdfi3od,werkhj23k"
    #date is str in form "YYYY-MM-DD HH:MM:SS.SSS"

#Comments(author Text, body TEXT, post TEXT, date TEXT);
    #post is the title of corresponding post
    #date is str in form "YYYY-MM-DD HH:MM:SS.SSS"

import sqlite3;
connection = sqlite3.connect('blog.db');



#precondition: name, pwd are str. priv is int [0,1]
#postcondition:
  #returns _id of new user if successful, else returns None
  #unsuccessful if given username already exits
def adduser(name, pwd, priv):
    #if isinstance(pwd, str):
    #    pass;
    q ="select Users.username from Users where username=%s"%(name)
    o = connection.execute(q)
    if(o != None):
        insert into Users values(name, pwd, priv)
        q = "select Users._id from Users where username =%s"%(name)
        return connection.execute(q)
    else:
        return None
        
#precondition: name, pwd are str
#postcondition:
  #returns True if pwd matches username
  #returns False if pwd doesn't match username
  #returns False if user with username of name DNE
def authuser(name, pwd):
    q = "select Users.username from Users where username=%s"%(name)
    username = connection.execute(q)
    if(username == None):
        return False
    q = "select Users.password from Users where username=%s"%(pwd)
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
    q = "select Users.username from Users where username=%s"%(name);
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
    q = "select Users.admin from Users where username=%s"%(name);
    priv = connection.execute(q)
    if(priv == None):
        return False;
    if(priv == 1):
        return True;
    else:
        return False;


#precondition: author,title,body are str
#              date is str in form "YYYY-MM-DD HH:MM:SS.SSS"
#postcondition:
    #returns True if post creation successful
    #returns False if user with username=author DNE;
    #returns False if post with same title already exists
def addpost(author, title, body, date):
    q = "select Users.username from Users where username=%s"%(author);
    athr = connection.execute(q);
    if(athr == None):
        return False;
    q = "select Posts.title from Posts where title=%s"%(title);
    tt = connection.execute(q);
    if(tt != None):
        return False;
    q = "INSERT into Users VALUES(%s,%s,%s,'',%s)"%(author, title, body, date);
    connection.execute(q);
    return True;
    
#precondition: title is str
#postcondition:
    #returns False if no post with given title exists
    #returns True if remove successful
def removepost(title):
    q = "select Posts.title from Posts where title=%s"%(title);
    t = connection.execute(q);
    if(t == None):
        return False;
    q = "delete from Posts where title=%s"%(title);
    connection.execute(q);
    return True;



#precondition: author,body,post,date are str
              #date is in form "YYYY-MM-DD HH:MM:SS.SSS" and is different from the date of all previously entered comments
              #post is title of post comment is attached to
#postcondition:
    #returns False if User with username of author DNE
    #returns False if Post with given title DNE
    #returns True if addition successful
def addcomment(author, body, post, date):
    q = "select Users.username from Users where username=%s"%(author);
    athr = connection.execute(q);
    if(athr == None):
        return False;
    q = "select Posts.comments from Posts where title=%s"%(post);
    comm = connection.execute(q);
    if(comm == None):
        return False;
    q = "INSERT into COMMENTS VALUES(%s,%s,%s,%s)"%(author,body,post,date);
    connection.execute(q);
    q = "select Comments._id from Comments where date=%s"%(date);
    cid = connection.execute(q);
    comm = comm + "," + cid;
    q = "UPDATE Posts SET comments=%s where title=%s"%(comm,post);
    connection.execute(q);
    return True;
    

#precondition:
    #cid is _id of comment to be removed
#postcondition:
    #returns False if comment with _id of cid DNE
    #returns True of removal successful
def removecomment(cid):
    q = "select Comments._id from Comments where _id=%s"%(cid);
    testid = connection.execute(q);
    if(testid == None):
        return False;
    q = "DELETE from Comments where _id =%s"%(cid);

#precondition:
    #attr is str and is the name of desired attribute, as given at top of this file
#postcondition:
    #returns False if commment DNE
    #otherwise, returns attribute attr of comment with _id
    #e.g. getCommentAttr("shfiu2wd234", "author") --> "Jim"
def getCommentAttr(_id, attr):
    q = "select Comments.%s where _id=%s"%(attr,_id);
    if(q == None):
        return False;
    return connection.execute(q);

#precondition:
#postcondition: returns string of all title posts
def getAllTitles():
    q = "select Posts.title from Posts";
    return connection.execute(q);


