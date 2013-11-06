from hashlib import sha512
from database import Database

__all__ = ['AuthDatabase']

class AuthDatabase(Database):

    def setup(self):
        self._execute(
            'CREATE TABLE users'
            '(username text, password text)')

    def auth_user(self, name, password):
        return bool(self._execute(
            'SELECT * FROM users WHERE '
            'username=? AND password=?',
            (name, password)))

    def exists(self, name):
        return bool(self._execute(
            'SELECT * FROM users WHERE '
            'username=?',
            (name,)))

    def add_user(self, name, password):
        if self._execute(
            'SELECT * FROM users WHERE '
            'username=?', (name,)): return False
        self._execute(
            'INSERT INTO users VALUES (?,?)',
            (name, password))
        return True

def crypto_hash(string):
    temp = sha512()
    temp.update(bytes(string, 'utf-8'))
    return temp.hexdigest()
