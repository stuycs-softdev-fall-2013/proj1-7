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

# Login stuff:

from werkzeug.security import generate_password_hash, check_password_hash
def register_user(username, pw):
	pw = pw.encode('ascii')
	conn = sqlite3.connect(db)
	c = conn.cursor()
	u = c.execute("SELECT username FROM logins WHERE username=(?)", (username,)).fetchone()
	if (u != None):
		conn.close()
		return False
	c.execute("INSERT INTO logins VALUES(?,?)", (username, encrypt(pw)))
	conn.commit()
	conn.close()

	return True

def check_user(username,pw):
	pw = pw.encode('ascii')
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT pw FROM logins WHERE username=(?)", (username,))
        u = c.fetchone()
        if u != None:
                ans = check_password_hash(u[0].encode('ascii'), pw)
                conn.close()		
                return ans
        return False

def change_pass(username, pw):
    pw = pw.encode('ascii')
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("UPDATE logins SET pw=? WHERE username=?",(encrypt(pw),username))
    conn.commit()

def encrypt(pw):
    return generate_password_hash(pw)
