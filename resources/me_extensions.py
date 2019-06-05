

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

    def createInventoryObject(self, object_class_str, kv_obj_reference):
        '''Create a new thing using the information filled in by the user in the popup'''

        # Get a dictionary of all user input strings
        # The keys must match with MongoEngine document definition attributes
        kwargs = self._getObjectCreationUserInput(kv_obj_reference)

        # Get the class (stored as an attribute) from self.session
        ObjectClass = getattr(self.session, object_class_str)

        # Create an instance of the new Inventory object and store it as a variable for later use
        new_object = ObjectClass(**kwargs)
        self.logDebug('DB Ops', f'Saved a new {new_object.description}')
        self.pop.dismiss()
        return new_object
