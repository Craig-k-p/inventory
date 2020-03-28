import json
import shutil


class IOHandler():
    def __init__(self):
        self.things = {}
        self.containers = {}
        self.file_hash = None

    def authenticate(self, user, pd):
        '''Method not needed with a local save.'''
        return True

    def isLoggedIn(self):
        '''Method not needed with a local save.'''
        return True

    def createInventoryObject(self, object_class_str, kv_obj_reference):
        '''Create a new thing using the information filled in by the user in the popup'''

        # Get a dictionary of all user input strings
        # The keys must match with those found in session.py
        data = self._getObjectCreationUserInput(kv_obj_reference)

        # # Get the proper method for saving data from self
        # ObjectClass = getattr(self, object_class_str)

        # # Create a new object and pass it to data_grid
        # new_object_doc = ObjectClass(data)
        self.logDebug('DB Ops', f'Saved a new {data["description"]}')
        self.pop.dismiss()

        # Add a new row with the new data to the user's screen
        self.sm.current_screen.data_grid.addDataRow(data)

        # Return the object's data
        return data

    def getObjects(self, object_class_str):
        '''Get objects in the user's inventory'''
        self.logInfo('__TEST__', f'app.getObjects called.')

        # Get 'thing' or 'container'
        objects = self.get(object_class_str)

        return objects

    def Thing(self, UID, data):
        '''Create a new thing'''
        self.logDebug('DB Ops', 'Creating a thing and saving it to the database')
        self.logDebug('DB Ops', f'{data}')
        self.things[UID] = data
        return data

    def Container(self, UID, data):
        '''Create a new container'''
        self.logDebug('DB Ops', 'Creating a container and saving it to the database')
        self.logDebug('DB Ops', f'{data}')
        self.containers[UID] = data
        return data

    def deleteObj(self, kind, obj_data):
        '''Delete the matching object.
            kind = 'thing' or 'container'
            matching_data = dict matching an existing object'''
        if kind == 'thing':
            if obj_data in self.things:
                self.things.pop(obj_data)

    def get(self, class_str):
        '''Return all user objects'''
        return []

    def prepareData(self, load):
        '''Prepare data for a save or from a load'''

        if load is True:
            pass

        # Prepare data for a save
        elif load is False:
            save_data = {'things':{},'containers':{}}
            for key in self.things:
                save_data['things'][key] = self.things[key]['doc']
            for key in self.containers:
                save_data['containers'][key] = self.containers[key]['doc']

            self.logDebug('IO Ops', f'Save data: {save_data}')


    def saveData(self):
        '''Hash user data to see if a save is needed.  Save and backup data if necessary'''

        with open(self.settings['save file'], 'w', encoding='utf-8') as f:
            self.prepareData(load=False)

    def loadData(self):
        '''Load and hash data to check if a save is needed'''

        # Catch errors if the file doesn't exist
        try:
            # Open the file in read mode with utf-8 encoding
            with open(self.settings['save file'], 'r', encoding='utf-8') as f:
                # Load the data as a dictionary
                objects = json.load(f)

        # If the file wasn't found, check for the backup file
        except FileNotFoundError:
            try:
                # Open the file in read mode with utf-8 encoding
                with open(self.settings['backup save file'], 'r', encoding='utf-8') as f:
                    # Load the data as a dictionary
                    objects = json.load(f)

            # If the file wasn't found, return empty dictionaries
            except FileNotFoundError:
                objects = {}
