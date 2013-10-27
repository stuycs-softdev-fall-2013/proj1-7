import sqlite3

def addUser(username, password):
    #used in the register page to create accounts
    #returns True or False depending on whether or not the account was created
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
    #user when logging in to verify account info
    connection = sqlite3.connect('OnceUponData.db')
    pass


def plusUserKarma(targetUser, sourceUser):
    #sourceUser is adding one to the karma of targetUser
    connection = sqlite3.connect('OnceUponData.db')
    pass


def minusUserKarma(targetUser, sourceUser):
    #sourceUser is subtracting one from the karma of targetUser
    connection = sqlite3.connect('OnceUponData.db')
    pass


def plusStoryKarma(storyID, user):
    #user is adding one to the karma of the story with the ID storyID
    connection = sqlite3.connect('OnceUponData.db')
    pass


def minusStoryKarma(storyID, user):
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
