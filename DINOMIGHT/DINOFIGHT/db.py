import sqlite3

db = "storyinator.db"


def add_story(user,title):
    #Add story to Storyinfo
    #Return the story id of the new story
    connection = sqlite3.connect(db)
    c = connection.cursor()
    c.execute("INSERT INTO storyinfo VALUES (?,?)", (user,title))#TODO: Check that there is no story with same title
    storyid = c.execute("SELECT storyid FROM storyinfo WHERE user=(?) AND title = (?)",(user,title)).fetchone();
    connection.commit()
    connection.close()
    return storyid

def add_sentence_to_story(user,story,sentence):
    #Add sentence to story
    #Return the setence id of the new sentence
    connection = sqlite3.connect(db)
    c = connection.cursor()
    c.execute("INSERT INTO sentenceinfo VALUES (?,?,?)", (user,story,sentence))
    sentenceid = c.execute("SELECT sentenceid FROM sentenceinfo WHERE user=(?) AND story = (?) AND sentence = (?)",(user,title,setence)).fetchone();
    connection.commit()
    connection.close()
    return sentenceid


