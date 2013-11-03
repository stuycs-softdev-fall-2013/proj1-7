from pymongo import MongoClient
from time import time

db = MongoClient().database
PAGE_LEN = 10 #number of stories per page

#create a new story
def create_story(author, title, first_line):
	line_id = db.lines.insert({'author': author, 'text': first_line,
							   'timestamp': time()})
	
	story_id = db.stories.insert({'author': author, 'title': title,
								  'lines': [line_id], 'timestamp': time(),
								  'karma': 0})

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
					 'owned': [], 'contributed': [], 'lines': [] })
	return True

#add a line to a story under an author's name
def add_line(author, line, story_id):
	line_id = db.lines.insert({'author': author, 'text': line,
							   'timestamp': time()})

	story_id = db.stories.update({'_id': story_id},
								 {'$push': {'lines': line}})

	db.users.update({'name': author},
					{'$push': {'lines': line_id}})

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

	return sorted_stories[(page_num-1) * PAGE_LEN : page_num * PAGE_LEN]

#return a page-worth of stories sorted by popularity
def get_popular_stories(page_num):
	stories = db.stories.find()

	sorted_stories = sorted(stories, key=lambda k: k['karma'])
	sorted_stories.reverse()

	return sorted_stories[(page_num-1) * PAGE_LEN : page_num * PAGE_LEN]

#try to login, return False on failure
def login(usern, passw):
	cursor = db.users.find({'name': usern, 'password': passw})

	users = [user for user in cursor]

	return len(users) != 0

def get_story(story_id):
	story = db.stories.find_one({'_id': story_id})

	return story
