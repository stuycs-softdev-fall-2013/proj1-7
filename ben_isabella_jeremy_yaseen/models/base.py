# Base objects object for interaction with MongoDB
from settings import DB_NAME
from pymongo import MongoClient


# Abstract class for objects in the database (posts, users)
class Model(object):

    def __init__(self, db, objects, obj=None):
        self.db = db
        self.objects = objects
        self._id = obj['_id']

    def remove(self):
        self.objects.remove({'_id': self._id})


class Collection(object):

    def __init__(self, name, model=Model):
        client = MongoClient()
        self.db = client[DB_NAME]
        self.objects = self.db[name]
        self.name = name
        self.model = model

    # Add support for fields
    def find(self, **kwargs):
        model = self.model
        return [model(self.db, self.objects, o) for o in \
                self.objects.find(kwargs)]

    def find_one(self, **kwargs):
        model = self.model
        return model(self.db, self.objects, self.objects.find_one(kwargs))

    def insert(self, **kwargs):
        id = self.objects.insert(kwargs)
        return self.find_one(_id=id)

    def remove(self, id):
        self.objects.remove({'_id': id})
