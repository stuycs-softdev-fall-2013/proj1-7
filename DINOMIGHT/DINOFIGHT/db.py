import sqlite3

db = "storyinator.db"

with open("create_tables", 'r') as table_text:
    connection = sqlite3.connect(db)
    for cmd in table_text.readlines():
        connection.execute(cmd)
    # need code to create the other tables, similar to the above
    connection.commit()
    connection.close()

def add_story(user,title):
    #Add story to Storyinfo
    #Return the story id of the new story
    connection = sqlite3.connect(db)
    c = connection.cursor()
    c.execute("INSERT INTO storyinfo VALUES(NULL, ?, ?)", (user,title))
    storyid = c.execute("SELECT storyid FROM storyinfo WHERE username=(?) AND title = (?)",(user,title)).fetchone();
    connection.commit()
    connection.close()
    return storyid[0] if len(storyid) > 0 else None

def add_sentence_to_story(user,storyid,sentence):
    #Add sentence to story
    #Return the sentence id of the new sentence
    connection = sqlite3.connect(db)
    c = connection.cursor()
    c.execute("INSERT INTO sentenceinfo VALUES(NULL, ?, ?, ?, 0)", (user, storyid, sentence))
    sentenceid = c.execute("SELECT sentenceid FROM sentenceinfo WHERE username=(?) AND storyid = (?) AND sentence = (?)",(user,storyid,sentence)).fetchone()
    connection.commit()
    connection.close()
    return sentenceid[0] if len(sentenceid) > 0 else None

def get_sentence(sentenceid):
    connection = sqlite3.connect(db)
    c = connection.cursor()
    sentence = c.execute("SELECT sentence FROM sentenceinfo WHERE sentenceid = (?)",(sentenceid,)).fetchone()
    connection.close()
    return sentence
    

def get_story(storyid):
    connection = sqlite3.connect(db)
    c = connection.cursor()
    sentences = c.execute("SELECT sentence FROM sentenceinfo WHERE storyid = (?)",(storyid,)).fetchall()
    story = ' '.join([sentence[0] for sentence in sentences])
    connection.close()
    return story

def get_storyid(title):
    connection = sqlite3.connect(db)
    c = connection.cursor()
    sid = c.execute("SELECT storyid FROM storyinfo WHERE title=(?)", (title,)).fetchone()
    connection.close()
    return sid[0] if len(sid) > 0 else None

def stories_by_user(username):
    connection = sqlite3.connect(db)
    c = connection.cursor()
    stories = c.execute("SELECT DISTINCT storyid FROM storyinfo WHERE username=(?)",(username,)).fetchall()
    connection.close()
    return [s[0] for s in stories]

def stories_with_user_contributions(username):
    connection = sqlite3.connect(db)
    c = connection.cursor()
    stories = c.execute("SELECT DISTINCT storyid FROM sentenceinfo WHERE username=(?)",(username,)).fetchall()
    connection.close()
    return [s[0] for s in stories]

def contributions_to_story(usern, storyid):
    connection = sqlite3.connect(db)
    c = connection.cursor()
    sentences = c.execute("SELECT sentenceid FROM sentenceinfo WHERE username=(?) AND storyid=(?)", (usern, storyid)).fetchall()
    return [s[0] for s in sentences]

def get_title(storyid):
    connection = sqlite3.connect(db)
    c = connection.cursor()
    return c.execute('SELECT title FROM storyinfo WHERE storyid=(?)', (storyid,)).fetchone()[0]

def incr_inappropriates(sentenceid):
    connection = sqlite3.connect(db)
    c = connection.cursor()
    old_inapprop = c.execute("SELECT num_inappropriate FROM sentenceinfo WHERE sentenceid=(?)",(sentenceid))
    c.execute("UPDATE sentenceinfo SET num_inappropriate=(?) WHERE sentenceid = (?)",(old_inapprop + 1,sentenceid))
    connection.commit()
    connection.close()

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
        u = u[0] if len(u) > 0 else ""
        if u != None:
                ans = check_password_hash(u.encode('ascii'), pw)
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
