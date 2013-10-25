from models import *
from datetime import datetime

if __name__ == '__main__':
    # Collections
    users = User()
    posts = Post()
    comms = Comment()

    # Creating users, note the date field
    u = users.insert(date=datetime.now(), username="Ben",password="iamsilly")
    u2 = users.insert(date=datetime.now(), username="Jeremy",password="YOLO")

    # Creating posts, note the date field
    p = u.add_post(date=datetime.now(), title="Hello World", body="My first post",
            tags=["best","post","ever"])
    p2 = u2.add_post(date=datetime.now(), title="Not a traditional title", body="I've posted before",
            tags=["original","stuff","bro"])

    # Adding comment to first post
    p.add_comment(date=datetime.now(), user="Jeremy", text="this is stupid")

    print "Getting comments from Jeremy..."
    for c in u2.get_comments():
        print c.user, ',', c.text

    print "Getting comments from Hello World post..."
    for c in p.get_comments():
        print c.user, ',', c.text

    print "Getting posts from newest to oldest..."
    for p in posts.get_by_date():
        print p.title, p.tags

    print "Getting posts with certain tag..."
    for p in posts.get_by_tag('original'):
        print p.title, p.tags

    # Cleaning up
    users.remove_all()
    posts.remove_all()
    comms.remove_all()
