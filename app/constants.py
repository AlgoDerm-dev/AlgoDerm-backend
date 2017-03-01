import os
#use os.environ.get('environmental variable')
DATABASE_URL = 'mysql+pymysql://root:@localhost:3306/AlgoDerm'
#mysql+pymysql://<username>:<password>@<host>
SECRET_KEY = 'its_a_secret'


class SimpleMultiDict(dict):
    def getlist(self, key):
        return self[key]

    def __repr__(self):
        return type(self).__name__ + '(' + dict.__repr__(self) + ')'
