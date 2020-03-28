class IOHandler():
    '''Used to keep the MongoEngine database methods separate from the Kivy graphics methods'''

    def authenticate(self, user, pd):
        '''Call methods in the UserSession classs to log the user in.'''
        return True

    def isLoggedIn(self):
        '''Method not needed with a local save.'''
        # if self.session.user is not None and self.session.client is not None:
        #     return True
        # else:
        #     return False
        return True

    def createInventoryObject(self, object_class_str, kv_obj_reference):
        '''Create a new thing using the information filled in by the user in the popup'''

        # Get a dictionary of all user input strings
        # The keys must match with MongoEngine document definition attributes
        kwargs = self._getObjectCreationUserInput(kv_obj_reference)

        # Get the proper method for saving data from self.SessionIO
        ObjectClass = getattr(self.SessionIO, object_class_str)

        # Create a new object and pass it to data_grid
        new_object_doc = ObjectClass(kwargs)
        self.logDebug('DB Ops', f'Saved a new {new_object_doc["description"]}')
        self.pop.dismiss()

        self.sm.current_screen.data_grid.addDataRow(new_object_doc)

        return new_object_doc

    def getObjects(self, object_class_str):
        '''Get objects in the user's inventory'''
        self.logInfo('__TEST__', f'app.getObjects called.')

        # Get 'thing' or 'container'
        objects = self.SessionIO.get(object_class_str)

        return objects
