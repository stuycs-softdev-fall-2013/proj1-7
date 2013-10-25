import sha
import sqlite3

userdata_filename = "keys.dat"
secret_key = "uniquellama"

#ensure db & table exist; should probably be fixed later
connection = sqlite3.connect(userdata_filename)
connection.execute("CREATE TABLE IF NOT EXISTS users(usern TEXT, passw TEXT)")
connection.commit()
connection.close()

def registerUser(usern, passw):
	passw = passw.encode('ascii')
	conn = sqlite3.connect(userdata_filename)
	c = conn.cursor()
	if (checkUser(usern, passw)):
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
		ans = u[0].encode('ascii') == encrypt(passw)
		conn.close()		
		return ans

	return False

# currently nonfunctional
def changePass(usern, passw):
	passw = passw.encode('ascii')
	print "should change %s password to %s"%(usern, passw)
	print "NOT YET IMPLEMENTED"
	conn = sqlite3.connect(userdata_filename)
	c = conn.cursor()
	c.execute("UPDATE users SET passw=(?) WHERE usern=(?)",(encrypt(passw),usern))
	conn.commit()

def encrypt(passw):
	encrypter = sha.new(passw)
	encrypter.update(secret_key)

	hashpass = encrypter.digest()

	return unicode(hashpass, errors='ignore') 
