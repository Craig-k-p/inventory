import json
import shutil
from resources.inventoryobjects import Thing, Container, InventoryObject
from graphics.py.account.row import ContainerDataRow, ThingDataRow


class InventoryHandler():
    def __init__(self):
        self.selected = None
        self.search_term = None
        self.data_was_loaded = False

    def createInventoryObject(self, object_class_str, kv_obj_reference):
        '''Create a new object using the popup user input'''

        if self._isValidPopupUserInput(kv_obj_reference) is True:
            # Get the method (thing or container) from InventoryHandler for creating
            # a new object
            createObject = getattr(self, object_class_str)

            # Get the data for the new object
            # Add the object's ID
            data = self._getObjectCreationUserInput(kv_obj_reference)
            data['ID'] = InventoryObject.getNewID()
            self.logInfo(f'User input:\n{json.dumps(data, indent=4)}')

            # Create a new object with user's input and dismiss the popup
            new_object = createObject(data)
            self.pop.dismiss()

            # Add a new row with the new data to the user's screen
            self.sm.current_screen.data_grid.addDataRow(new_object)

            InventoryObject.debugDump()

            # Return the object's data
            return data

        else:
            pass

    def thing(self, data):  # createObject
        '''Create a new thing and assign its container'''
        self.logDebug(f'Creating a thing with ID {data["ID"]}:')
        new_thing = Thing(data)
        if self.data_was_loaded == True:
            self.selected.addThing(new_thing.ID)
            InventoryObject.changeMade()
        return new_thing

    def container(self, data):  # createObject
        '''Create a new container'''
        self.logDebug(f'Creating a container with ID {data["ID"]}:')
        new_container = Container(data)
        if self.data_was_loaded == True:
            InventoryObject.changeMade()
        return new_container

    def loadData(self):
        '''Make a backup of the save file and load and hash the user's data'''

        if self.data_was_loaded == True:
            return

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
            containers[key]['ID'] = int(key)
            self.container(containers[key])
        for key in things:
            things[key]['ID'] = int(key)
            self.thing(things[key])

        for key in Container.objs:
            ContainerDataRow(Container.objs[key])
        for key in Thing.objs:
            ThingDataRow(Thing.objs[key])


        self.data_was_loaded = True

        InventoryObject.checkLoad()


    def saveData(self):
        '''Hash user data to see if a save is needed.  Save and backup data if necessary'''

        if InventoryObject.wasChanged() == True:
            self.logDebug('Changes were made. Getting data to save')
            data = InventoryObject.getSaveData()
            self.logDebug('Saving the JSON data to the save file')
            # Open the save file and write json data to the file
            with open(self.settings['save file'], 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)
        else:
            self.logInfo('No changes made. Skipping save')

    def select(self, selection):
        '''Set the selected object directly or by using the ID'''

        if selection == None:
            self.selected = None
            InventoryObject.selected = None
        elif isinstance(selection, Container):
            self.selected = selection
            InventoryObject.selected = selection
        else:
            self.selected = InventoryObject.getByID(selection)
            InventoryObject.selected = selection
            self.logInfo(f'Selected {self.selected}')

    def getObjects(self):
        for ID in InventoryObject.objs:
            self.logDebug(f'{InventoryObject.objs[ID].description} has grid: {InventoryObject.objs[ID].grid}')
