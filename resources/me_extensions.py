

class MongoEngineExtensions():
    '''Used to keep the MongoEngine database methods separate from the Kivy graphics methods'''

    def authenticate(self, user, pd):
        '''Call methods in the UserSession classs to log the user in.'''
        self.logInfo('DB AUTH', f'Checking credentials for {user}')
        is_authenticated = self.session.login(user, pd)
        del user, pd
        return is_authenticated

    def createUser(self, user, em, pd):
        '''Call methods in the UserSession class to create a user and log the user in'''
        self.logInfo('DB Ops', 'Creating a new user..')
        was_created = self.session.createUser(user, pd)
        if was_created is True:
            is_authenticated = self.session.login(user, pd)
            del user, pd
            if is_authenticated is True:
                return True
            else:
                self.logError('DB Ops', 'User was created in MongoDB but was unable to log in!')
                return False
        else:
            self.logError('DB Ops', 'MongoDB user creation attempt failed!')
            return False

    def isLoggedIn(self):
        if self.session.user is not None and self.session.client is not None:
            return True
        else:
            return False
