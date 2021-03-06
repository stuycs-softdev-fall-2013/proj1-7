import sqlite3

__all__ = ['Database']

class Database(object):

    def __init__(self, name):
        self._name = name
    
    def _execute(self, command, args=None):
        connection = sqlite3.connect(self._name)
        cursor = connection.cursor()

        if args is None:
            out = cursor.execute(command).fetchall()
        else:
            out = cursor.execute(command, args).fetchall()
        
        connection.commit()
        connection.close()
        return out
