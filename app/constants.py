import os
#use os.environ.get('environmental variable')
DATABASE_URL = 'mysql+pymysql://root:@localhost:3306/AlgoDerm'
#mysql+pymysql://<username>:<password>@<host>
SECRET_KEY = 'its_a_secret'

# Access Key ID:
AWS_KEY = 'AKIAJRXH42WGMAYYJCPQ'
# Secret Access Key:
AWS_SECRET = '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'
class SimpleMultiDict(dict):
    def getlist(self, key):
        return self[key]

    def __repr__(self):
        return type(self).__name__ + '(' + dict.__repr__(self) + ')'
