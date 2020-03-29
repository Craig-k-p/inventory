import json
import shutil


class IOHandler():
    def __init__(self):
        self.things = {}
        self.containers = {}
        self.data_hash = None
        self.data = None

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

        self.logInfo('IO Ops', f'User input:\n{json.dumps(data, indent=4)}')

        # # Get the proper method for saving data from self
        createObject = getattr(self, object_class_str)

        self.logDebug('IO Ops', f'{self.things}')
        self.logDebug('IO Ops', f'{self.containers}')

        # Create a new object with user's input and dismiss the popup
        new_object_doc = createObject(self._getUID(), data)
        self.logDebug('IO Ops', f'Saved a new {data["description"]}')
        self.pop.dismiss()

        self.logDebug('IO Ops', f'{self.things}')
        self.logDebug('IO Ops', f'{self.containers}')

        # Add a new row with the new data to the user's screen
        self.sm.current_screen.data_grid.addDataRow(data)

        self.logDebug('IO Ops', f'It doesn\'t look like the data was stored for file writing')

        # Return the object's data
        return data

    def getObjects(self, object_class_str):
        '''Get objects in the user's inventory'''
        self.logInfo('IO Ops', f'app.getObjects called with object_class_str {object_class_str}.')

        # Change the class string to a usable key for the data dict
        new_object_class_str = 'things' if object_class_str == 'Thing' else 'containers'
        # Load any available data into self.data
        self.loadData()

        return self.data[new_object_class_str]

    def Thing(self, UID, data):
        '''Create a new thing'''
        self.logDebug('IO Ops', 'Creating a thing and saving it to the database..')
        self.logDebug('IO Ops', f'\n{json.dumps(data, indent=4)}')
        self.things[UID] = data
        return data

    def Container(self, UID, data):
        '''Create a new container'''
        self.logDebug('IO Ops', 'Creating a container and saving it to the database')
        self.logDebug('IO Ops', f'\n{json.dumps(data, indent=4)}')
        self.containers[UID] = data
        return data

    def deleteObj(self, kind, obj_data):
        '''Delete the matching object.
            kind = 'thing' or 'container'
            matching_data = dict matching an existing object'''
        if kind == 'thing':
            if obj_data in self.things:
                self.things.pop(obj_data)


    def loadData(self):
        '''Make a backup of the save file and load and hash the user's data'''

        # Catch errors if the file doesn't exist
        try:
            self.logDebug('IO Ops', f'Attempting to load from the save file')
            # Open the file in read mode with utf-8 encoding
            with open(self.settings['save file'], 'r', encoding='utf-8') as f:
                # Load the data as a dictionary
                self.data = json.load(f)
                self.logInfo('IO Ops', f'loaded data:\n{json.dumps(self.data, indent=4)}')

        except FileNotFoundError:
            # If the load data is None, set the data to its default
            self.logDebug('IO Ops', f'No save file found')
            self.data = {
                'containers': {},
                'things': {}
            }

        self.data_hash = hash(str(self.data))
        self.things = self.data['things']
        self.containers = self.data['containers']


    def saveData(self):
        '''Hash user data to see if a save is needed.  Save and backup data if necessary'''

        self.logDebug('IO Ops', f'data: {self.data}')
        self.logDebug('IO Ops', f'data hash: {hash(str(self.data))}')
        self.logDebug('IO Ops', f'Previous hash: {self.data_hash}')

        # Check if any changes were made to the user's data
        if hash(str(self.data)) != self.data_hash:
            self.logDebug('IO Ops', f'Data to be saved didn\'t match old data. Saving..')

            self.logDebug('IO Ops', f'Saving the JSON data to the save file')
            # Open the save file and write json data to the file
            with open(self.settings['save file'], 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)

        else:
            self.logInfo('IO Ops', 'Data hashes matched. Skipping save')
