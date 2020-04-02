import json
import shutil
from resources.inventoryobjects import Thing, Container, InventoryObject


class InventoryHandler():
    def __init__(self):
        self.loaded_data_hash = None
        self.selected = None
        self.search_term = None
        self.loaded_data = None

    def authenticate(self, user, pd):
        '''Method not needed with a local save.'''
        return True

    def isLoggedIn(self):
        '''Method not needed with a local save.'''
        return True

    def createInventoryObject(self, object_class_str, kv_obj_reference, is_new=False):
        '''Create a new object using the popup user input'''

        if self._isValidPopupUserInput(kv_obj_reference) is True:
            # Get the method (thing or container) from InventoryHandler for creating
            # a new object
            createObject = getattr(self, object_class_str)

            # Get the data for the new object
            # Add the object's UID
            data = self._getObjectCreationUserInput(kv_obj_reference)
            data['UID'] = self.getUniqueID()
            self.logInfo(f'User input:\n{json.dumps(data, indent=4)}')

            # Create a new object with user's input and dismiss the popup
            new_object = createObject(data, is_new)
            self.pop.dismiss()
            self.logDebug(f'Saved a new {new_object}')

            # Add a new row with the new data to the user's screen
            self.sm.current_screen.data_grid.addDataRow(new_object)

            # Return the object's data
            return data

        else:
            pass

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

    def thing(self, data, is_new=False):
        '''Create a new thing and assign its container'''
        self.logDebug(f'Creating a thing with UID {data["UID"]}:')
        new_thing = Thing(data)
        if is_new == True:
            self.selected.addThing(new_thing)
        return new_thing

    def container(self, data, is_new=False):
        '''Create a new container'''
        self.logDebug(f'Creating a container with UID {data["UID"]}:')
        new_container = Container(data)
        if is_new == True:
            self.select(new_container)
        return new_container

    def deleteObject(self, obj):
        '''Delete the object'''
        # Deselect the object
        if obj == self.selected:
            self.selected == None

        self.logInfo(f'Deleting {obj}')
        obj.delete()


    def loadData(self):
        '''Make a backup of the save file and load and hash the user's data'''

        # Catch errors if the file doesn't exist
        try:
            self.logDebug(f'Attempting to load from the save file')
            # Open the file in read mode with utf-8 encoding
            with open(self.settings['save file'], 'r', encoding='utf-8') as f:
                # Load the data as a dictionary
                inventory = json.load(f)
                self.logInfo(f'loaded data:\n{json.dumps(inventory, indent=4)}')

        except FileNotFoundError:
            # If the load data is None, set the data to its default
            self.logDebug(f'No save file found')
            inventory = {
                'container': {},
                'thing': {}
            }

        # Create the inventory objects with the loaded data
        containers = inventory['container']
        things = inventory['thing']
        for key in containers:
            containers[key]['UID'] = key
            self.container(containers[key])
        for key in things:
            things[key]['UID'] = key
            self.thing(things[key])

        self.loaded_data_hash = hash(str(inventory))
        self.loaded_data = inventory


    def saveData(self):
        '''Hash user data to see if a save is needed.  Save and backup data if necessary'''

        self.logDebug(f'data: {json.dumps(self.inventory, indent=4)}')
        self.logDebug(f'data hash: {hash(str(self.inventory))}')
        self.logDebug(f'Previous hash: {self.loaded_data_hash}')

        # # Check if any changes were made to the user's data
        # if hash(str(self.inventory)) != self.loaded_data_hash:
        #     self.logDebug(f'Data to be saved didn\'t match old data. Saving..')

        #     self.logDebug(f'Saving the JSON data to the save file')
        #     # Open the save file and write json data to the file
        #     with open(self.settings['save file'], 'w', encoding='utf-8') as f:
        #         json.dump(self.inventory, f, ensure_ascii=False, indent=4)

        # else:
        #     self.logInfo('Data hashes matched. Skipping save')

    def select(self, selection):
        '''Set the selected object directly or by using the UID'''

        if selection == None:
            self.selected = None
            InventoryObject.selected = None
        elif isinstance(selection, Container):
            self.selected = selection
            InventoryObject.selected = selection
        else:
            self.selected = InventoryObject.getByUID(selection)
            InventoryObject.selected = selection
            self.logInfo(f'Selected {self.selected}')

    def verifyObjectsLoaded(self):
        '''Verify that the data has been loaded from the file'''
        self.logDebug('Verifying that the objects were loaded')
        if self.loaded_data != None:
            return True
        else:
            self.loadData()
            return True
