import json, os, shutil

from resources.inventoryobjects import Thing, Container, InventoryObject
from graphics.row import ContainerDataRow, ThingDataRow
from graphics.screens import AccountOverviewScreen, ContainerOverviewScreen


class InventoryHandler():
    def __init__(self):
        self.data_screens = (AccountOverviewScreen, ContainerOverviewScreen)
        self.data_was_loaded = False
        InventoryObject.app = self
        self.inventoryobject = InventoryObject

    def createInventoryObject(self, object_class_str, kv_obj_reference):
        '''Create a new object using the popup user input'''

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

        # Return the object's data
        return data

    def thing(self, data):  # createObject
        '''Create a new thing and assign its container'''
        self.logDebug(f'Creating a thing with ID {data["ID"]}:')
        new_thing = Thing(data)

        if self.data_was_loaded == True:
            # Add the thing to the last selected container
            self.selection.getLastContainer().getObj().addThing(new_thing.ID)
            # Set the changes_made flag to True for saving purposes
            InventoryObject.changeMade()
        return new_thing

    def doesFileExist(self, file_name):
        '''Make sure we aren't overwriting any saved files'''
        file_name = file_name.strip() + '.inventory'

        for file in self.files:
            if file == file_name:
                return True

        return False

    def container(self, data):  # createObject
        '''Create a new container'''
        self.logDebug(f'Creating a container with ID {data["ID"]}:')
        new_container = Container(data)

        if self.data_was_loaded == True:
            # Set the changes_made flag to True for saving purposes
            InventoryObject.changeMade()
        return new_container

    def getSaveFiles(self):
        '''Get the save file names'''
        self.files = []
        for file in os.listdir(self.settings['save file path']):
            if file.endswith(".inventory"):
                self.files.append(file)

        self.logDebug(self.files)

        return self.files

    def getObjects(self):
        for ID in InventoryObject.objs:
            self.logDebug(f'{InventoryObject.objs[ID].description} has grid: {InventoryObject.objs[ID].grid}')

    def loadData(self):
        '''Load the user's data'''

        if self.data_was_loaded == True:
            return

        self.logDebug(self.user_file)

        # Catch errors if the file doesn't exist
        try:
            self.logDebug(f'Attempting to load from the save file')
            # Open the file in read mode with utf-8 encoding
            with open(self.user_file, 'r', encoding='utf-8') as f:
                # Load the data as a dictionary
                inventory = json.load(f)
                self.logInfo(f'loaded data:\n{json.dumps(inventory, indent=4)}')

        except FileNotFoundError:
            try:
                with open(self.settings['save file path'] + self.user_file) as f:
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

        # Reset the InventoryObject._changes_made attribute to False to avoid saving the same data
        InventoryObject.resetChangeMade()
        InventoryObject.checkLoad()

    def restart(self):
        '''Reset the app to the load file screen. Save user data to disk and remove data from memory'''
        # Save user data
        self._saveData()
        # Remove user data from memory
        self._cleanup()
        # Create new widgets and start at the home screen
        self._setup()

    def select(self, selection):
        '''Set the selected object directly or by using the ID.
           Select nothing by passing None as the argument.'''

        if selection == None:
            self.selected = None
            InventoryObject.selected.deselect()
        elif isinstance(selection, (Container, Thing)):
            self.selected = selection
            InventoryObject.selected = selection
        else:
            self.selected = InventoryObject.getByID(selection)
            InventoryObject.selected = self.selected
            self.logInfo(f'Selected {self.selected}')

        if isinstance(self.selected, Container):
            self.context_container_selection = self.selected

        self.logDebug(f'SELECTED: {self.selected}')

    def updateObjectData(self, popup, object_class_str):
        '''Update an inventory item's data from user input'''
        self.logDebug('Updating the object\'s data')
        popup.inventory_object.description = popup.description.text
        popup.inventory_object.usd_value = popup.usd_value.text
        popup.inventory_object.weight = popup.weight.text

        try:
            popup.inventory_object.location = popup.location.text
        except AttributeError:
            pass

        popup.inventory_object.addTags(popup.tags.text)
        popup.inventory_object.widget.assignValues()

        if object_class_str == 'thing':
            popup.inventory_object.getContainer().widget.assignValues()

    def getStat(self,
                container_count=False,
                inventory_count=False,
                value=False,
                weight=False,
                tags=False
                ):
        '''Return information about the inventory as a string'''
        if container_count == True:
            return str(len(Container.objs))

        elif inventory_count == True:
            return str(len(Thing.objs))

        elif value == True:
            value = 0
            for key in Container.objs:
                value += round(Container.objs[key].getValue(), 0)
            return f"${format(int(value), ',.0f')}"

        elif weight == True:
            weight = 0
            for key in Container.objs:
                weight += round(Container.objs[key].getWeight(), 0)
            return f"{format(int(weight), ',.0f')} lbs"

        elif tags == True:
            return InventoryObject.getTopTags()

        else:
            self.logError('No flags were set to True')
            return 'N/A'

    def _cleanup(self):
        '''Remove the inventory that was loaded previously'''
        self.user_file = None
        InventoryObject.cleanup()
        Container.cleanup()
        Thing.cleanup()
        self.selection.cleanup()

        while len(self.sm.screens) > 0:
           self.sm.remove_widget(self.sm.screens[0])

        self.data_was_loaded = False
        InventoryObject.resetChangeMade()

    def _saveData(self):
        '''Save data if necessary'''

        if self.inventoryobject.wasChangeMade() == True:
            self.logDebug('Changes were made. Getting data to save')
            data = InventoryObject.getSaveData()
            self.logDebug('Saving the JSON data to the save file')
            # Open the save file and write json data to the file
            if '.inventory' not in self.user_file:
                self.user_file += '.inventory'
            if self.settings['save file path'] not in self.user_file:
                self.user_file = self.settings['save file path'] + self.user_file
            with open(self.user_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)
        else:
            self.logInfo('No changes made. Skipping save')
