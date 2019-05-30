

class MongoEngineExtensions():
    '''Used to keep the MongoEngine database methods separate from the Kivy graphics methods'''

    def authenticate(self, user, pd):
        self.logInfo('DB AUTH', f'Checking credentials for {user}')

        self.session.login(user, pd)
