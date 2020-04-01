import json
import shutil


class InventoryHandler():
    def __init__(self):
        self.inventory_hash = None
        self.inventory_kv = {}
        self.inventory = None
        self.selected_object = None

    def authenticate(self, user, pd):
        '''Method not needed with a local save.'''
        return True

    def isLoggedIn(self):
        '''Method not needed with a local save.'''
        return True

    def setTags(self, str_tags):
        '''Take a string of user-input tags and turn them into a list of searchable
           tags'''
        self.logDebug(f'Modifying user-input tags {str_tags}')

        if str_tags == '':
            return []

        # Remove surrounding blank characters and split the tags up by spaces
        str_tags = str_tags.strip()
        tags = str_tags.split(' ')
        # Replace underscores with spaces
        for n in range(len(tags)):
            tags[n] = tags[n].replace('_', ' ')

        return tags

    def createInventoryObject(self, object_class_str, kv_obj_reference):
        '''Create a new object using the popup user input'''

        # Get a dictionary of all user input strings
        # The keys must match with those found in session.py

        if self._isValidPopupUserInput(kv_obj_reference) is True:
            data = self._getObjectCreationUserInput(kv_obj_reference)
            self.logInfo(f'User input:\n{json.dumps(data, indent=4)}')

            # Take the user-input tags and make sure they're searchable
            data['tags'] = self.setTags(data['tags'])

            # Get the method (thing or container) from InventoryHandler for creating a new object
            createObject = getattr(self, object_class_str)

            # Create a new object with user's input and dismiss the popup
            UID = self.getUniqueID()
            new_object_doc = createObject(data, UID)
            self.logDebug(
                f'Saved a new {self.inventory[object_class_str][UID]["description"]}'
            )
            self.pop.dismiss()

            self.logDebug(
                f'New data: {json.dumps(self.inventory[object_class_str][UID], indent=4)}'
            )

            # Add a new row with the new data to the user's screen
            self.sm.current_screen.data_grid.addDataRow(data, UID)

            # Return the object's data
            return data

        else:
            pass

    def getObjects(self, object_class_str):
        '''Get objects in the user's inventory'''
        self.logInfo(f'app.getObjects called with object_class_str {object_class_str}.')

        if self.inventory == None:
            # Load any available data into self.data
            self.loadData()

        return self.inventory[object_class_str]

    def getUniqueID(self):
        '''Increment self.uid_counter and return the value'''

        # Make sure only unique IDs are used
        invalid = True
        while invalid:
            self.uid_counter += 1  # Increment the ID counter
            self.logInfo(f'app.uid_counter incremented to {self.uid_counter}')

            # Do nothing if UID already exists
            if str(self.uid_counter) in self.inventory['thing'].keys():
                self.logDebug(f'{self.uid_counter} found in things')
                pass
            # Do nothing if UID already exists
            elif str(self.uid_counter) in self.inventory['container'].keys():
                self.logDebug(f'{self.uid_counter} found in containers')
                pass
            # Return the UID if it doesn't exist
            else:
                self.logInfo(f'Returning app.uid_counter {self.uid_counter}')
                return str(self.uid_counter)

    def thing(self, data, UID):
        '''Create a new thing and assign its container'''
        self.logDebug(f'Creating a thing with UID {UID}:')
        self.logDebug(f'\n{json.dumps(data, indent=4)}')

        self.inventory['thing'][UID] = data

        # If there is a selected object, be sure to update the container and thing data
        if self.selected_object != None:
            self.inventory['thing'][UID]['in'] = self.selected_object
            self.inventory['container'][self.selected_object]['contains'].append(UID)
        else:
            self.inventory['thing'][UID]['in'] = None
        return data

    def container(self, data, UID):
        '''Create a new container'''
        self.logDebug(f'Creating a container with UID {UID}:')
        self.logDebug(f'\n{json.dumps(data, indent=4)}')
        self.inventory['container'][UID] = data
        if 'contains' not in self.inventory['container'][UID].keys():
            self.inventory['container'][UID]['contains'] = []
        return data

    def deleteObject(self, UID):
        '''Delete the object in self.data using the UID'''
        UID = str(UID)
        if UID in self.inventory['thing']:
            del self.inventory['thing'][UID]
        elif UID in self.inventory['container']:
            del self.inventory['container'][UID]
        else:
            raise KeyError(f'UID [{UID}] not found in self.inventory')

        # Deselect the object
        if UID == self.selected_object:
            self.selected_object == None

        self.logInfo(f'Deleted object with UID {UID}')


    def loadData(self):
        '''Make a backup of the save file and load and hash the user's data'''

        # Catch errors if the file doesn't exist
        try:
            self.logDebug(f'Attempting to load from the save file')
            # Open the file in read mode with utf-8 encoding
            with open(self.settings['save file'], 'r', encoding='utf-8') as f:
                # Load the data as a dictionary
                self.inventory = json.load(f)
                self.logInfo(f'loaded data:\n{json.dumps(self.inventory, indent=4)}')

        except FileNotFoundError:
            # If the load data is None, set the data to its default
            self.logDebug(f'No save file found')
            self.inventory = {
                'container': {},
                'thing': {}
            }

        # Make sure the list of contained things is in the dictionary
        for container in self.inventory['container'].keys():
            if 'contains' not in self.inventory['container'][container]:
                self.inventory['container'][container]['contains'] = []
            if 'in' not in self.inventory['container'][container]:
                self.inventory['container'][container]['tags'] = []

        # Make sure things have the "in" key
        for thing in self.inventory['thing'].keys():
            if 'in' not in self.inventory['thing'][thing]:
                self.inventory['thing'][thing]['in'] = None
            if 'tags' not in self.inventory['thing'][thing]:
                self.inventory['thing'][thing]['tags'] = []

        self.inventory_hash = hash(str(self.inventory))


    def saveData(self):
        '''Hash user data to see if a save is needed.  Save and backup data if necessary'''

        self.logDebug(f'data: {json.dumps(self.inventory, indent=4)}')
        self.logDebug(f'data hash: {hash(str(self.inventory))}')
        self.logDebug(f'Previous hash: {self.inventory_hash}')

        # Check if any changes were made to the user's data
        if hash(str(self.inventory)) != self.inventory_hash:
            self.logDebug(f'Data to be saved didn\'t match old data. Saving..')

            self.logDebug(f'Saving the JSON data to the save file')
            # Open the save file and write json data to the file
            with open(self.settings['save file'], 'w', encoding='utf-8') as f:
                json.dump(self.inventory, f, ensure_ascii=False, indent=4)

        else:
            self.logInfo('Data hashes matched. Skipping save')

    def select(self, UID):
        '''Set the selected object using the object's UID'''
        self.selected_object = UID
        self.logInfo(f'Selected container with ID {UID}')
