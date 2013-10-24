import sha
import sqlite3

userdata_filename = "keys.dat"
secret_key = "uniquellama"

connection = sqlite3.connect(userdata_filename)
connection.execute("CREATE TABLE IF NOT EXISTS users(usern TEXT, pasw TEXT)")
connection.commit()
connection.close()

def registerUser(usern, passw): 
	conn = sqlite3.connect(userdata_filename)

	c = conn.cursor()


	for user in result:
		if user[0] == usern:
			conn.close()
			#the user already exists
			return False

	c.execute("insert into users values(?,?)", (usern, encrypt(passw)))
	conn.commit()
	conn.close()

	return True

def checkUser(usern,passw):
	passw = passw.encode('ascii')

	#get userlist
	conn = sqlite3.connect('keys.dat')
	c = conn.cursor()

	#c.execute("select * from users where ")
	c.execute("select * from users where usern=(?)", usern)
	for user in c:
		if user[0] == usern:
			ans = user[1] == encrypt(passw)
			conn.close()

			return ans

	return False

def changePass(usern, passw):
	passw = passw.encode('ascii')
	

def encrypt(passw):
	encrypter = sha.new(passw)
	encrypter.update(secret_key)

	hashpass = encrypter.digest()

	return unicode(hashpass, errors='ignore') 
