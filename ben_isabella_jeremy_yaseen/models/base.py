# Models and Collections (abstract classes)
# Models represent individual entries in a database, while Collections
# represent entire collections in a databse
from pymongo import MongoClient
from datetime import datetime
from settings import DB_NAME
from utils import pretty_date


class Model(object):

    def __init__(self, db, collection, obj=None):
        self.db = db
        self.collection = collection
        self.date = obj['date']
        self._id = obj['_id']

    # Gets _id
    def get_id(self):
        return self._id

    # Gets the date converted to a string
    def get_datestring(self):
        return self.date.strftime('%A, %B %d')

    # Gets the time delta converted to string
    def get_deltastring(self):
        return pretty_date(self.date)

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
        if objs:
            return [model(self.db, self.objects, o) for o in objs]
        return None

    # Returns a model list corresponding to find in database
    def find(self, **kwargs):
        return self.to_objects(self.objects.find(kwargs))

    # Returns a model object corresponding to find_one in database
    def find_one(self, **kwargs):
        model = self.model
        objs = self.objects.find_one(kwargs)
        if objs:
            return model(self.db, self, objs)
        return None

    # Inserts objects into collection
    def insert(self, **kwargs):
        new_args = kwargs
        new_args['date'] = datetime.now()
        id = self.objects.insert(new_args)
        return self.find_one(_id=id)

    # Updates objects in the collection
    def update(self, conds, **kwargs):
        self.objects.update(conds, {'$set': kwargs})

    # Remove all objects in the collection
    def remove_all(self):
        self.objects.remove()

    # Remove objects based on keyword parameters
    def remove(self, **kwargs):
        self.objects.remove(kwargs)

    # Return model objects forted by certain values
    def sort_by(self, sort_vals):
        return self.to_objects(self.objects.find({}).sort(sort_vals))

    # Gets anything by date
    def get_by_date(self):
        return self.sort_by([('date', -1)])
