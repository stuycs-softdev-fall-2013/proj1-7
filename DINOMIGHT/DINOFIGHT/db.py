import sqlite3

db = "storyinator.db"

with open("create_tables", 'r') as table_text:
    connection = sqlite3.connect(db)
    for cmd in table_text.readlines():
        connection.execute(cmd);
    # need code to create the other tables, similar to the above
    connection.commit()
    connection.close()

def add_story(user,title):
    #Add story to Storyinfo
    #Return the story id of the new story
    connection = sqlite3.connect(db)
    c = connection.cursor()
    c.execute("INSERT INTO storyinfo VALUES (?,?)", (user,title))
    storyid = c.execute("SELECT storyid FROM storyinfo WHERE user=(?) AND title = (?)",(user,title)).fetchone();
    connection.commit()
    connection.close()
    return storyid

def add_sentence_to_story(user,storyid,sentence):
    #Add sentence to story
    #Return the sentence id of the new sentence
    connection = sqlite3.connect(db)
    c = connection.cursor()
    c.execute("INSERT INTO sentenceinfo VALUES (?,?,?,?)", (user,storyid,sentence,0))
    sentenceid = c.execute("SELECT sentenceid FROM sentenceinfo WHERE user=(?) AND story = (?) AND sentence = (?)",(user,title,sentence)).fetchone();
    connection.commit()
    connection.close()
    return sentenceid

def get_sentence(sentenceid):
    connection = sqlite3.connect(db)
    c = connection.cursor()
    sentence = c.execute("SELECT sentence FROM sentenceinfo WHERE sentenceid = (?)",(sentenceid,)).fetchone();
    connection.commit()
    connection.close()
    return sentence
    

def get_story(storyid):
    connection = sqlite3.connect(db)
    c = connection.cursor()
    sentences = c.execute("SELECT sentence FROM sentenceinfo WHERE storyid = (?)"),(storyid,).fetchall();
    story = ''
    for sentence in sentences:
        story += sentence
    connection.commit()
    connection.close()
    return story

def db_filename():
    return db
