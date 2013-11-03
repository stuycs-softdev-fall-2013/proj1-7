from bson.objectid import ObjectId
from pymongo import MongoClient
from time import time

db = MongoClient().database
PAGE_LEN = 10 #number of stories per page

#create a new story
def create_story(author, title, first_line):
	story_id = db.stories.insert({'author': author, 'title': title,
								  'lines': [], 'timestamp': time(),
								  'karma': 0})

	line_id = add_line(author, first_line, story_id)

	db.users.update({'name': author},
					{'$push': {'lines': line_id, 'stories': story_id}})

#try to register, return False on failure
def register(usern, passw, passwcf):
	if passw != passwcf:
		return False

	matched_users = [user for user in db.users.find({'name': usern})]

	if len(matched_users) != 0:
		return False

	db.users.insert({'name': usern, 'password': passw,
					 'stories': [], 'lines': [] })
	return True

#add a line to a story under an author's name
def add_line(author, line, story_id):
	line_id = db.lines.insert({'author': author, 'text': line,
							   'timestamp': time(), 'story': story_id})

	story_id = db.stories.update({'_id': story_id},
								 {'$push': {'lines': line_id}})

	db.lines.update({'_id': line_id},
					{'$set': {'story': story_id}})

	db.users.update({'name': author},
					{'$push': {'lines': line_id}})

	return line_id

#return stories with a given ordering
def get_stories(order, page_num):
	if order == 'recent':
		return get_recent_stories(page_num)

	if order == 'popular':
		return get_popular_stories(page_num)

	return False

#return a page-worth of stories sorted by recency
def get_recent_stories(page_num):
	stories = db.stories.find()

	sorted_stories = sorted(stories, key=lambda k: k['timestamp'])
	sorted_stories.reverse()

	#replace line ids with line text
	for story in sorted_stories:
		for i in range(len(story['lines'])):
			story['lines'][i] = get_line_text(story['lines'][i])

	return sorted_stories[(page_num-1) * PAGE_LEN : page_num * PAGE_LEN]

#return a page-worth of stories sorted by popularity
def get_popular_stories(page_num):
	stories = db.stories.find()

	sorted_stories = sorted(stories, key=lambda k: k['karma'])
	sorted_stories.reverse()

	#replace line ids with line text
	for story in sorted_stories:
		for i in range(len(story['lines'])):
			story['lines'][i] = get_line_text(story['lines'][i])

	return sorted_stories[(page_num-1) * PAGE_LEN : page_num * PAGE_LEN]

#try to login, return False on failure
def login(usern, passw):
	cursor = db.users.find({'name': usern, 'password': passw})

	users = [user for user in cursor]

	return len(users) != 0

def get_story(story_id):
	story_id = ObjectId(story_id)
	story = db.stories.find_one({'_id': story_id})

	return story

def get_line_text(line_id):
	line = db.lines.find_one({'_id': line_id})

	return line['text']

def get_line_story(line_id):
	line = db.lines.find_one({'_id': line_id})

	return db.stories.find_one({'_id': line['story']})

def get_user(usern):
	return db.users.find_one({'name': usern.encode('UTF-8')})

def get_owned_stories(usern):
	user = get_user(usern)

	stories = [db.stories.find_one({'_id': story_id})
			   for story_id in user['stories']]

	return stories

def get_contrib_stories(usern):
	user = get_user(usern)

	stories = set([get_line_story(line_id) for line_id in user['lines']])

	return stories

def reset():
	db.users.drop()
	db.lines.drop()
	db.stories.drop()
