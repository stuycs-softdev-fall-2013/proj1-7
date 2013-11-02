# Models and Collections for blog posts
from models.base import Collection, Model
from models.comment import Comment
from settings import POST_COLLECTION


class PostModel(Model):

    def __init__(self, db, collection, obj):
        super(PostModel, self).__init__(db, collection, obj)
        self.user = obj['user']
        self.title = obj['title']
        self.body = obj['body']
        self.tags = obj['tags']
        self.date = obj['date']
        self.comments = Comment()

    # Adds a comment on this post
    def add_comment(self, **kwargs):
        return self.comments.insert(post_id=self._id, **kwargs)

    # Gets comments on this post
    def get_comments(self):
        return self.comments.find(post_id=self._id)

    # Use for removing comments by the user who created them, or by the poster
    def remove_comments(self, **kwargs):
        self.comments.remove(**kwargs)

    # Removes self and the comments
    def remove(self):
        self.remove_comments(post_id=self._id)
        super(PostModel, self).remove()


class Post(Collection):

    def __init__(self):
        super(Post, self).__init__(POST_COLLECTION, PostModel)

    # Return posts sorted by date for front page
    def get_by_date(self):
        return self.sort_by([('date', -1)])
