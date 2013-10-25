from models import *

if __name__ == '__main__':
    users = User()
    u = users.insert(username="Ben",password="iamsilly")
    u2 = users.insert(username="Jeremy",password="YOLO")
    p = u.add_post(title="Hello World", body="My first post",
            date="somedate",tags=["best","post","ever"])
    p.add_comment(user="Jeremy",text="this is stupid",
            date="somedate")
    for c in u2.get_comments():
        print c.user, ',', c.text

    for c in p.get_comments():
        print c.user, ',', c.text

    users.remove_all()
    for p in Post().find():
        p.remove()
