

class MongoEngineExtensions():
    '''Used to keep the MongoEngine database methods separate from the Kivy graphics methods'''

    def authenticate(self, user, pswd):
        self.logInfo('DB AUTH', f'Checking credentials for {user}')
