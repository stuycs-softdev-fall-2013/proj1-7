# Models and Collections for comments
from models.base import Collection, Model
from models.comment import Comment


class PostModel(Model):

    def __init__(self, db, objects, obj):
        super(PostModel, self).__init__(db, objects, obj)
        self.user = obj['user']
        self.user = obj['title']
        self.body = obj['body']
        self.date = obj['date']
        self.tags = obj['tags']
        self.comments = Comment()

    def add_comment(self, **kwargs):
        new_args = kwargs
        new_args['post_id'] = self._id
        return self.comments.insert(**new_args)

    def get_comments(self):
        return self.comments.find(post_id=self._id)

    def remove_comments(self, **kwargs):
        self.comments.remove(**kwargs)

    def remove(self):
        self.remove_comments(post_id=self._id)
        super(PostModel, self).remove()


class Post(Collection):

    def __init__(self):
        super(Post, self).__init__('posts', PostModel)
