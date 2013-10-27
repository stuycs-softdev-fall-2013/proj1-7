# Models and Collections for comments
from models.base import Collection, Model
from settings import COMMENT_COLLECTION


class CommentModel(Model):

    def __init__(self, db, objects, obj):
        super(CommentModel, self).__init__(db, objects, obj)
        self.user = obj['user']
        self.text = obj['text']
        self.date = obj['date']
        self.post_id = obj['post_id']


class Comment(Collection):

    def __init__(self):
        super(Comment, self).__init__(COMMENT_COLLECTION, CommentModel)
