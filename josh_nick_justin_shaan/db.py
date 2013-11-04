

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
  #returns True of new user if successful, else returns False
  #unsuccessful if given username already exits
def adduser(name, pwd, priv):
    #if isinstance(pwd, str):
    #    pass;
    q ="select Users.username from Users where username='%s'"%(name)
    o = connection.execute(q)
    if(o isinstance sqlite3.cursor):
        q = "insert into Users values('%s','%s',%i)"%(name, pwd, priv)
        connection.execute(q)
        return True
    else:
        return False
        
#precondition: name, pwd are str
#postcondition:
  #returns True if pwd matches username
  #returns False if pwd doesn't match username
  #returns False if user with username of name DNE
def authuser(name, pwd):
    q = "select Users.password from Users where username='%s'"%(name)
    password = connection.execute(q)
    if(password == ""):
        return False
    if(password == pwd):
        return True
    else:
        return False
    
#precondition: name is str
#postcondition:
    #returns True if user successfully removed
    #returns False if user DNE
def removeuser(name):
    q = "select Users.username from Users where username='%s'"%(name);
    usr = connection.execute(q);
    if(usr == ""):
        return False;
    q = "DELETE from Users where username='%s'"%(name);
    connection.execute(q);
    return True;

#precondition: username, newPwd are str
#postcondition: changes password of User with username to newPwd
def changePassword(username, newPwd):
    q = "select Users.password from Users where username='%s'"%(username);
    ps = connection.execute(q);
    if(ps == ""):
        return False;
    q = "UPDATE Users SET password='%s' where username='%s'"%(newPwd, username);
    connection.execute(q);
    return True;
    

#precondition: usr is str
#postcondition:
    #returns True if user is an admin
    #returns False if user is not admin
    #returns False if user DNE
def isAdmin(name):
    q = "select Users.admin from Users where username='%s'"%(name);
    priv = connection.execute(q)
    if(priv == ""):
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
    q = "select Users.username from Users where username='%s'"%(author);
    athr = connection.execute(q);
    if(athr == ""):
        return False;
    q = "select Posts.title from Posts where title='%s'"%(title);
    tt = connection.execute(q);
    if(tt != ""):
        return False;
    q = "INSERT into Users VALUES(%s,%s,%s,'',%s)"%(author, title, body, date);
    connection.execute(q);
    return True;
    
#precondition: title is str
#postcondition:
    #returns False if no post with given title exists
    #returns True if remove successful
def removepost(title):
    q = "select Posts.title from Posts where title='%s'"%(title);
    t = connection.execute(q);
    if(t == ""):
        return False;
    q = "delete from Posts where title='%s'"%(title);
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
    q = "select Users.username from Users where username='%s'"%(author);
    athr = connection.execute(q);
    if(athr == ""):
        return False;
    q = "select Posts.comments from Posts where title='%s'"%(post);
    comm = connection.execute(q);
    if(comm == ""):
        return False;
    q = "INSERT into COMMENTS VALUES(%s,%s,%s,%s)"%(author,body,post,date);
    connection.execute(q);
    q = "select Comments.date from Comments where date='%s'"%(date);
    cid = connection.execute(q);
    comm = comm + "," + cid;
    q = "UPDATE Posts SET comments='%s' where title='%s'"%(comm,post);
    connection.execute(q);
    return True;
    

#precondition:
    #cid is date of comment to be removed
#postcondition:
    #returns False if comment with _id of cid DNE
    #returns True of removal successful
def removecomment(date):
    q = "select Comments.date from Comments where date='%s'"%(date);
    testid = connection.execute(q);
    if(testid == ""):
        return False;
    q = "DELETE from Comments where _id ='%s'"%(cid);


#precondition:
#postcondition: returns string of all title posts
def getAllTitles():
    q = "select Posts.title from Posts";
    return connection.execute(q);

print 0
print removeuser("jduda")
print 1
print adduser("jduda", "asdf", 1)
print 2
print authuser("jduda", "apple")
print 3
print authuser("jduda", "asdf")
print 4
print changePassword("jduda", "banana")
print 5
print authuser("jduda", "asdf")
print 6
print authuser("jduda", "banana")
print 7
print isAdmin("jduda")
print 8
print getUserAttr("jduda", "password")
print 9

connection.close()
