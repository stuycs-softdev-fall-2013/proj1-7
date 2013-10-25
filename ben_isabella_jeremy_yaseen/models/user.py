# Models and Collections for users
from models.base import Collection, Model
from models.post import Post
from models.comment import Comment


class UserModel(Model):

    def __init__(self, db, objects, obj):
        super(UserModel, self).__init__(db, objects, obj)
        self.username = obj['username']
        self.password = obj['password']
        self.posts = Post()
        self.comments = Comment()

    def change_password(self, oldpass, newpass):
        if oldpass == self.password:
            self.password = newpass

    def get_blog_posts(self):
        return self.posts.find(user=self.username)

    def get_comments(self):
        return self.comments.find(user=self.username)

    def add_post(self, **kwargs):
        new_args = kwargs
        new_args['user'] = self.username
        return self.posts.insert(**new_args)


class User(Collection):

    def __init__(self):
        super(User, self).__init__('users', UserModel)
