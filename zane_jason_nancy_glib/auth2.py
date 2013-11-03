from flask import session
from bson.objectid import ObjectId
from pymongo import MongoClient
from time import time
from math import ceil

db = MongoClient().database
PAGE_LEN = 5 #number of stories per page

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
	errcode = []
	if passw != passwcf:
		errcode.append('passw-mismatch')

	matched_users = [user for user in db.users.find({'name': usern})]

	if len(matched_users) != 0:
		errcode.append('usern-used')

	if not errcode:
		db.users.insert({'name': usern, 'password': passw,
					 	 'stories': [], 'lines': [], 'upvoted': [],
					 	 'downvoted': [] })
	return errcode

#add a line to a story under an author's name
def add_line(author, line, story_id):
	story_id = ObjectId(story_id)

	line_id = db.lines.insert({'author': author, 'text': line,
							   'timestamp': time(), 'story': story_id})

	story_id = db.stories.update({'_id': story_id},
								 {'$push': {'lines': line_id}})

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

#get a story object with line-ids replaced with line text
def get_story(story_id):
	story_id = ObjectId(story_id)
	story = db.stories.find_one({'_id': story_id})

	#replace line ids with line text
	for i in range(len(story['lines'])):
		story['lines'][i] = get_line_text(story['lines'][i])

	return story

#get the text from a line
def get_line_text(line_id):
	line = db.lines.find_one({'_id': line_id})

	return line['text']

#get the story of a line
def get_line_story(line_id):
	line = db.lines.find_one({'_id': line_id})

	return db.stories.find_one({'_id': line['story']})

#get a
def get_user(usern):
	return db.users.find_one({'name': usern.encode('UTF-8')})

def get_owned_stories(usern):
	user = get_user(usern)

	stories = [db.stories.find_one({'_id': story_id})
			   for story_id in user['stories']]

	return stories

def get_contrib_stories(usern):
	user = get_user(usern)

	stories = []
	for line_id in user['lines']:
		stories.append(get_line_story(line_id))
	
	set_stories= []
	for s in stories:
		if s not in set_stories:
			set_stories.append(s)

	return set_stories

def reset():
	db.users.drop()
	db.lines.drop()
	db.stories.drop()

def handle_login(form):
	if login(form['username'], form['password']):
		session['user'] = form['username']
		return True
	
	return False

def get_num_pages():
	stories = [s for s in db.stories.find()]
	return int(ceil(len(stories) / PAGE_LEN))

def upvote(usern, story_id):
	story_id = ObjectId(story_id)
	user = get_user(usern)

	if story_id not in user['upvoted']:
		db.stories.update({'_id': story_id},
					  	  {'$inc': {'karma': 1}})
		db.users.update({'_id': user['_id']},
						{'$push': {'upvoted': story_id}})
		if story_id in user['downvoted']:
			db.users.update({'_id': user['_id']},
							{'$pull': {'downvoted': story_id}})
			db.stories.update({'_id': story_id},
					  	  	  {'$inc': {'karma': 1}})

def downvote(usern, story_id):
	story_id = ObjectId(story_id)
	user = get_user(usern)

	if story_id not in user['downvoted']:
		db.stories.update({'_id': story_id},
					  	  {'$inc': {'karma': -1}})
		db.users.update({'_id': user['_id']},
						{'$push': {'downvoted': story_id}})
		if story_id in user['upvoted']:
			db.users.update({'_id': user['_id']},
							{'$pull': {'upvoted': story_id}})
			db.stories.update({'_id': story_id},
					  	  	  {'$inc': {'karma': -1}})



