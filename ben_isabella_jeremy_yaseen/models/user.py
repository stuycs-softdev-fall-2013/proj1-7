# Models and Collections for users
from models.base import Collection, Model
from models.post import Post
from models.comment import Comment


class UserModel(Model):

    def __init__(self, db, objects, obj):
        super(UserModel, self).__init__(db, objects, obj)
        self.username = obj['username']
        self.password = obj['password']
        self.date = obj['date']
        self.posts = Post()
        self.comments = Comment()

    # Change password with authentication--username auth to be done 
    # in middleware
    def change_password(self, oldpass, newpass):
        if oldpass == self.password:
            self.password = newpass

    # Get blog posts made by this user, and with other arguments
    def get_blog_posts(self, **kwargs):
        return self.posts.find(user=self.username, **kwargs)

    # Get comments made by the user, with other parameters
    def get_comments(self, **kwargs):
        return self.comments.find(user=self.username, **kwargs)

    # Adds a post under the users page
    def add_post(self, **kwargs):
        new_args = kwargs
        new_args['user'] = self.username
        return self.posts.insert(**new_args)


class User(Collection):

    def __init__(self):
        super(User, self).__init__('users', UserModel)

    # Checks if a specific user exists
    def exists(self, username):
        return len(self.find(username=username)) > 0
