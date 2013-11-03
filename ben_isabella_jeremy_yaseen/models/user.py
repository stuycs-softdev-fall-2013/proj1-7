# Models and Collections for users
from models.base import Collection, Model
from models.post import Post
from models.comment import Comment
from settings import USER_COLLECTION


class UserModel(Model):

    def __init__(self, db, collection, obj):
        super(UserModel, self).__init__(db, collection, obj)
        self.username = obj['username']
        self.password = obj['password']
        self.voted = obj['voted']
        self.posts = Post()
        self.comments = Comment()

    # Change password with authentication--username auth to be done 
    # in middleware
    def change_password(self, oldpass, newpass):
        if oldpass == self.password:
            self.password = newpass
            self.collection.update({'_id': self.get_id()}, password=newpass)
            return True
        return False

    # Vote a post up, cannot do this more than once for any given post
    def vote_up(self, post_id):
        if not post_id in self.voted:
            p = self.posts.find_one(_id=post_id)
            p.vote_up()
            self.voted.append(post_id)
            self.collection.update({'_id': self.get_id()}, voted=self.voted)

    # Adds a post under the users page
    def add_post(self, **kwargs):
        return self.posts.insert(user=self.username, **kwargs)

    # Get blog posts made by this user, and with other arguments
    def get_blog_posts(self, **kwargs):
        return self.posts.find(user=self.username, **kwargs)

    # Get comments made by the user, with other parameters
    def get_comments(self, **kwargs):
        return self.comments.find(user=self.username, **kwargs)


class User(Collection):

    def __init__(self):
        super(User, self).__init__(USER_COLLECTION, UserModel)

    def insert(self, **kwargs):
        return super(User, self).insert(voted=[], **kwargs)

    # Checks if a specific user exists
    def exists(self, username):
        return self.find_one(username=username) is not None
