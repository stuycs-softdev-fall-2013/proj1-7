# Models and Collections for users
from models.base import Collection, Model
from models.post import Post


class UserModel(Model):

    def __init__(self, db, objects, obj):
        super(UserModel, self).__init__(db, objects, obj)
        self.username = obj['username']
        self.password = obj['password']
        self.posts = Post()

    # In middleware, change page should only be available if username is correct
    def change_password(self, oldpass, newpass):
        return 1

    def get_start_date(self):
        return 1

    def get_blog_posts(self):
        return self.posts.find(user=self.username)

    def get_comments(self):
        db = self.db
        results = [o for o in db.posts.find({'comments': {'$elemMatch':
                                {'user': self.username}}},
                        fields={'_id': False, 'comments': True})]
        comments = []
        for r in results:
            for c in r['comments']:
                if c['user'] == self.username:
                    comments.append(c)
        return comments


class User(Collection):

    def __init__(self):
        super(User, self).__init__('users', UserModel)
