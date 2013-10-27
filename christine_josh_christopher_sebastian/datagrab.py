import sqlite3

def addUser(username, password):
    #used in the register page to create accounts
    #returns False if the username already exists
    connection = sqlite3.connect('OnceUponData.db')
    q = "select * from account_info where username='%s'"%(username)
    cursor = connection.execute(q)
    results = [line for line in cursor]
    if len(results) == 0:
        q = "insert into account_info values('%s', '%s', 0, '', '', '', '', '')"%(username,password)
        connection.execute(q)
        connection.commit()
        return True
    else:
        return False


def authenticate(username, password):
    #used when logging in to verify account info
    #returns whether or not the username/password combo is valid
    connection = sqlite3.connect('OnceUponData.db')
    q = "select password from account_info where username='%s'"%(username)
    cursor = connection.execute(q)
    results = [line for line in cursor]
    if len(results) == 1 and password == results[0][0]:
        return True
    else:
        return False
    


def likeEdit(editID, sourceUser):
    #sourceUser is adding one to the karma of edit with editID
    #returns False if a user tries to like their own edit or like an edit twice
    connection = sqlite3.connect('OnceUponData.db')
    q = "select user from edits where id='%s'"%(editID)
    cursor = connection.execute(q)
    targetUser = [line for line in cursor]
    targetUser = targetUser[0][0].encode('ascii','inore')
    if targetUser == sourceUser:
        return False
    q = "select liked_edits from account_info where username='%s'"%(sourceUser)
    cursor = connection.execute(q)
    likedEdits = [line for line in cursor]
    if likedEdits[0][0] != '':
        likedEdits = likedEdits[0][0].split(',')
        for edit in likedEdits:
            if edit == "%i"%(editID):
                return False
        updatedLikedEdits = ",".join(likedEdits) + ",%i"%(editID)
    else:
        updatedLikedEdits = "%i"%(editID)
    q = "select karma from account_info where username='%s'"%(targetUser) 
    cursor = connection.execute(q)
    currentKarma = [line for line in cursor]
    q = "update account_info set karma=%i where username='%s'"%(currentKarma[0][0] + 1,targetUser)
    connection.execute(q)
    q = "update account_info set liked_edits='%s' where username='%s'"%(updatedLikedEdits,sourceUser)
    connection.execute(q)
    connection.commit()
    return True


def dislikeEdit(editID, sourceUser):
    #sourceUser is subtracting one from the karma of edit with editID
    #returns False if a user tries to dislike their own edit or dislike an edit twice
    connection = sqlite3.connect('OnceUponData.db')
    pass


def likeStory(storyID, user):
    #user is adding one to the karma of the story with the ID storyID
    connection = sqlite3.connect('OnceUponData.db')
    pass


def dislikeEdit(storyID, user):
    #user is subtracting one from the karma of the story with the ID storyID
    connection = sqlite3.connect('OnceUponData.db')
    pass


def newEdit(storyID, user):
    #user adds a new edit to the story with ID storyID
    connection = sqlite3.connect('OnceUponData.db')    
    pass


def newStory(storyID, user):
    #user forks the story with ID storyID
    connection = sqlite3.connect('OnceUponData.db')    
    pass
