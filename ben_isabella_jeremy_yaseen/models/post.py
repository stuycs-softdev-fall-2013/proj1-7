# Object for base posts
from models.base import Collection, Model


# Object for a blog post
class PostModel(Model):

    def __init__(self, db, objects, obj):
        super(PostModel, self).__init__(db, objects, obj)
        self.user = obj['user']
        self.body = obj['body']
        self.date = obj['date']
        self.tags = obj['tags']
        self.comments = obj['comments']

    def remove_comment(self, user, date):
        comments = []
        for c in self.comments:
            if c['user'] != user and c['date'] != date:
                comments.append(c)
        self.comments = comments
        self.objects.update({'_id': self._id},
                {'$set': {'comments': comments}})


class Post(Collection):

    def __init__(self):
        super(Post, self).__init__('posts', PostModel)
