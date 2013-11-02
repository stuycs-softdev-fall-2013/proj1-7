#import sha
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

userdata_filename = "keys.dat"

#ensure db & table exist; should probably be fixed later
connection = sqlite3.connect(userdata_filename)
connection.execute("CREATE TABLE IF NOT EXISTS users(usern TEXT, passw TEXT)")
connection.commit()
connection.close()

def registerUser(usern, passw):
	passw = passw.encode('ascii')
	conn = sqlite3.connect(userdata_filename)
	c = conn.cursor()
	u = c.execute("select usern from users where usern=(?)", (usern,)).fetchone()
	if (u != None):
		conn.close()
		return False
	c.execute("insert into users values(?,?)", (usern, encrypt(passw)))
	conn.commit()
	conn.close()

	return True

def checkUser(usern,passw):
	passw = passw.encode('ascii')

	#get userlist
	conn = sqlite3.connect(userdata_filename)
	c = conn.cursor()
	c.execute("select passw from users where usern=(?)", (usern,))
	u = c.fetchone()
	if u != None:
		ans = check_password_hash(u[0].encode('ascii'), passw)
		conn.close()		
		return ans

	return False

def changePass(usern, passw):
	passw = passw.encode('ascii')
	conn = sqlite3.connect(userdata_filename)
#        print conn.execute('SELECT passw from users WHERE usern=?', (usern,))
	c = conn.cursor()
	c.execute("UPDATE users SET passw=? WHERE usern=?",(encrypt(passw),usern))
	conn.commit()

def encrypt(passw):
        return generate_password_hash(passw)
