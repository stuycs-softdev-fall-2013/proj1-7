from pymongo import MongoClient

client = MongoClient()
db = client.db

def load_stories():
	d = {'stories':[]}

	d['stories'] = [["Title %d"%(x+1), "Line.", "Another line.",
					 "A third line."] for x in range(5)]

	return d

def login(usern, passw):
	cursor = db.users.find({'usern': usern, 'passw': passw},
							fields={'_id': False})
	users = [user for user in cursor]

	return len(users) > 0
