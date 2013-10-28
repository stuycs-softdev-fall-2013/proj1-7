import sqlite3

def addUser(username, password):
    #used in the register page to create accounts
    #returns False if the username already exists
    connection = sqlite3.connect('OnceUponData.db')
    q = "select * from account_info where username=?"
    cursor = connection.execute(q, [username])
    results = [line for line in cursor]
    if len(results) == 0:
        q = "insert into account_info values(?, ?, 0, '', '', '', '', '')"
        connection.execute(q, [username, password])
        connection.commit()
        return True
    else:
        return False


def authenticate(username, password):
    #used when logging in to verify account info
    #returns whether or not the username/password combo is valid
    connection = sqlite3.connect('OnceUponData.db')
    q = "select password from account_info where username=?"
    cursor = connection.execute(q, [username])
    results = [line for line in cursor]
    if len(results) == 1 and password == results[0][0]:
        return True
    else:
        return False
    


def likeEdit(editID, sourceUser):
    #sourceUser is adding one to the karma of edit with editID
    #returns False if a user tries to like their own edit or like an edit twice
    connection = sqlite3.connect('OnceUponData.db')
    q = "select user from edits where id=?"
    cursor = connection.execute(q, [editID])
    targetUser = [line for line in cursor]
    targetUser = targetUser[0][0].encode('ascii','inore')
    if targetUser == sourceUser:
        return False
    q = "select liked_edits from account_info where username=?"
    cursor = connection.execute(q, [sourceUser])
    likedEdits = [line for line in cursor]
    q = "select disliked_edits from account_info where username=?"
    cursor = connection.execute(q, [sourceUser])
    dislikedEdits = [line for line in cursor]
    if likedEdits[0][0] != '':
        likedEdits = likedEdits[0][0].split(',')
        for edit in likedEdits:
            if edit == "%i"%(editID):
                return False
        updatedLikedEdits = ",".join(likedEdits) + ",%i"%(editID)
    else:        
        updatedLikedEdits = "%i"%(editID)

    if dislikedEdits[0][0] != '':
        dislikedEdits = dislikedEdits[0][0].split(',')
        for edit in dislikedEdits:
            if edit == "%i"%(editID):
                return False
            
    q = "select karma from account_info where username=?"
    cursor = connection.execute(q, [targetUser])
    currentKarma = [line for line in cursor]
    q = "update account_info set karma=? where username=?"
    connection.execute(q, currentKarma[0][0]+1, [targetUser])
    q = "update account_info set liked_edits=? where username=?"
    connection.execute(q, [updatedLikedEdits, sourceUser])
    connection.commit()
    return True


def dislikeEdit(editID, sourceUser):
    #sourceUser is subtracting one from the karma of edit with editID
    #returns False if a user tries to dislike their own edit or dislike an edit twice
    connection = sqlite3.connect('OnceUponData.db')
    q = "select user from edits where id=?"
    cursor = connection.execute(q, [editID])
    targetUser = [line for line in cursor]
    targetUser = targetUser[0][0].encode('ascii','inore')

    if targetUser == sourceUser:
        return False
    q = "select liked_edits from account_info where username=?"
    cursor = connection.execute(q, [sourceUser])
    likedEdits = [line for line in cursor]
    q = "select disliked_edits from account_info where username=?"
    cursor = connection.execute(q, [sourceUser])
    dislikedEdits = [line for line in cursor]

    
    if likedEdits[0][0] != '':
        likedEdits = likedEdits[0][0].split(',')
        for edit in likedEdits:
            if edit == "%i"%(editID):
                return False

    if dislikedEdits[0][0] != '':
        dislikedEdits = dislikedEdits[0][0].split(',')
        for edit in dislikedEdits:
            if edit == "%i"%(editID):
                return False
        updatedDislikedEdits = ",".join(dislikedEdits) + ",%i"%(editID)
    else:
        updatedDislikedEdits = "%i"%(editID)

    q = "select karma from account_info where username=?"
    cursor = connection.execute(q, [targetUser])
    currentKarma = [line for line in cursor]
    q = "update account_info set karma=? where username=?"
    connection.execute(q, currentKarma[0][0]-1, [targetUser])
    q = "update account_info set disliked_edits=? where username=?"
    connection.execute(q, [updatedDislikedEdits, sourceUser])
    connection.commit()
    return True


def likeStory(storyID, user):
    #user is adding one to the karma of the story with the ID storyID
    connection = sqlite3.connect('OnceUponData.db')
    pass


def dislikeStory(storyID, user):
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
