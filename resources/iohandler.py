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
        '''Create a new object using the popup user input'''

        # Get a dictionary of all user input strings
        # The keys must match with those found in session.py
        test = self._isValidPopupUserInput(kv_obj_reference)

        if test is True:
            data = self._getObjectCreationUserInput(kv_obj_reference)

            self.logInfo('IO Ops', f'User input:\n{json.dumps(data, indent=4)}')

            # # Get the proper method from self for saving data
            createObject = getattr(self, object_class_str)

            # Create a new object with user's input and dismiss the popup
            UID = self.getUniqueID()
            new_object_doc = createObject(data, UID)
            self.logDebug('IO Ops', f'Saved a new {data["description"]}')
            self.pop.dismiss()

            self.logDebug('IO Ops', f'New data: {json.dumps(self.data, indent=4)}')

            # Add a new row with the new data to the user's screen
            self.sm.current_screen.data_grid.addDataRow(data, UID)

            # Return the object's data
            return data

        else:
            pass

    def getObjects(self, object_class_str):
        '''Get objects in the user's inventory'''
        self.logInfo(
            'IO Ops',
            f'app.getObjects called with object_class_str {object_class_str}.'
        )

        if self.data == None:
            # Load any available data into self.data
            self.loadData()

        # Change the class string to a usable key for the data dict
        data = self.things if object_class_str == 'Thing' else self.containers

        return data

    def getUniqueID(self):
        '''Increment self.uid_counter and return the value'''

        # Make sure only unique IDs are used
        invalid = True
        while invalid:
            self.uid_counter += 1  # Increment the ID counter
            self.logInfo('DEBUG', f'app.uid_counter incremented to {self.uid_counter}')

            # Do nothing if UID already exists
            if str(self.uid_counter) in self.things.keys():
                self.logDebug('DEBUG', f'{self.uid_counter} found in self.things.keys()')
                pass
            # Do nothing if UID already exists
            elif str(self.uid_counter) in self.containers.keys():
                self.logDebug('DEBUG', f'{self.uid_counter} found in self.containers.keys()')
                pass
            # Return the UID if it doesn't exist
            else:
                self.logInfo('kvLogic', f'Returning app.uid_counter {self.uid_counter}')
                return str(self.uid_counter)

    def Thing(self, data, UID):
        '''Create a new thing'''
        self.logDebug('IO Ops', f'Creating a thing with UID {UID}:')
        self.logDebug('IO Ops', f'\n{json.dumps(data, indent=4)}')
        self.things[UID] = data
        return data

    def Container(self, data, UID):
        '''Create a new container'''
        self.logDebug('IO Ops', f'Creating a container with UID {UID}:')
        self.logDebug('IO Ops', f'\n{json.dumps(data, indent=4)}')
        self.containers[UID] = data
        return data

    def deleteObj(self, UID):
        '''Delete the object in self.data using the UID'''
        UID = str(UID)
        if UID in self.things:
            del self.things[UID]
        elif UID in self.containers:
            del self.containers[UID]
        else:
            raise KeyError(f'UID [{UID}] not found in self.things or self.containers')

        self.logInfo('IO Logic', f'Deleted object with UID {UID}')


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

        self.logDebug('IO Ops', f'data: {json.dumps(self.data, indent=4)}')
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
