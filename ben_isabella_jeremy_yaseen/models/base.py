# Models and Collections (abstract classes)
# Models represent individual entries in a database, while Collections
# represent entire collections in a databse
from pymongo import MongoClient
from settings import DB_NAME


class Model(object):

    def __init__(self, db, objects, obj=None):
        self.db = db
        self.objects = objects
        self._id = obj['_id']

    # Removes the object from database
    def remove(self):
        self.objects.remove({'_id': self._id})


class Collection(object):

    def __init__(self, name, model=Model):
        client = MongoClient()
        self.db = client[DB_NAME]
        self.objects = self.db[name]
        self.name = name
        self.model = model

    # Converts list of dict objects to Model objects
    def to_objects(self, objs):
        model = self.model
        return [model(self.db, self.objects, o) for o in objs]

    # Returns a model list corresponding to find in database
    def find(self, **kwargs):
        return self.to_objects(self.objects.find(kwargs))

    # Returns a model object corresponding to find_one in database
    def find_one(self, **kwargs):
        model = self.model
        return model(self.db, self.objects, self.objects.find_one(kwargs))

    # Return model objects forted by certain values
    def sort_by(self, sort_vals):
        return self.to_objects(self.objects.find({}).sort(sort_vals))

    # Inserts objects into collection
    def insert(self, **kwargs):
        id = self.objects.insert(kwargs)
        return self.find_one(_id=id)

    # Remove all objects in the collection
    def remove_all(self):
        self.objects.remove()

    # Remove objects based on keyword parameters
    def remove(self, **kwargs):
        self.objects.remove(kwargs)
