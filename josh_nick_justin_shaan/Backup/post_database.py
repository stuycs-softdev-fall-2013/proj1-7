from database import Database

__all__=['PostDatabase']

class PostDatabase(Database):

    def setup_database(self):
        return self._execute(
            'CREATE TABLE posts (time text, title text, content text)')

    def get_posts(self):
        return self._execute(
            'SELECT * FROM posts ORDER BY time')

    def add_post(self, title, content):
        return self._execute(
            'INSERT INTO posts VALUES (?,?,?)',
            (time(), title, content))
        
import datetime
def time():
    return datetime.datetime.now().isoformat()[:-7]

