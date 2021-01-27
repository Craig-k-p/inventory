import json, os, shutil

from resources.inventory import Inventory
from graphics.screens2 import InventoryScreen


class DataHandler():
    default_settings = {
        'encrypt color': (.79, .51, .51, 1),
        'kv popup file': 'graphics/popups.kv',
        'popup auto_dismiss': False,
        'popup size_hint': (None, None),
        'popup size': (600, 600),
        'row heading color': (.15, .15, .15, 1),
        'row color': (.2, .2, .2, 1),
        'row selected color': (.2, .75, .8, 1),
        'row heading text color': (.95, .95, .95, 1),
        'startup kv files': [
            'graphics/screens.kv',
            'graphics/screens.kv'
        ],
        'standard color': (.79, .73, .51, 1),
        'text color': (1, 1, 1, 1),
        'val_col_width': 110,
        'weight_col_width': 60
    }
    def __init__(self):
        self.data_screen = InventoryScreen
        self.data_was_loaded = False
        self.is_new_inventory = False
        Inventory.app = self
        self.inventory = Inventory

    def createInventoryObject(self, object_data):  # createObject
        '''Create a new container'''
        object_data['screen_manager'] = self.inventory_sm

        self.logDebug(f'Creating {object_data}:')

        new_inventory = Inventory(**object_data)

        self.logDebug(new_inventory.screen)

        if self.data_was_loaded == True or self.is_new_inventory:
            container = self.selection.getContainer().getObj()
            if isinstance(container, Inventory):
                container.addInventory(new_inventory.ID)
            # Set the changes_made flag to True for saving purposes
            Inventory.changeMade()
        return new_inventory

    def createInventory(self, kv_obj_reference):
        '''Create a new object using the popup user input'''

        # Get the data for the new object
        # Add the object's ID
        data = self._getNewInventoryUserInput(kv_obj_reference)
        data['ID'] = Inventory.getNewID()
        self.logInfo(f'User input:\n{json.dumps(data, indent=4)}')

        # Create a new object with user's input and dismiss the popup
        new_object = self.createInventoryObject(data)
        self.pop.dismiss()

        # Add a new row with the new data to the user's screen
        self.app_sm.current_screen.data_grid.addDataRow(new_object)

        # Return the object's data
        return data

    def doesFileExist(self, file_name, encrypted=False):
        '''Make sure we aren't overwriting any saved files'''
        file_name = file_name.strip() + '.inventory'

        if encrypted == True:
            file_name = 'e.' + file_name

        self.logDebug(f'Checking for duplicate file against {file_name}')
        for file in self.files:
            self.logDebug(file)
            if file == file_name:
                return True

        return False

    def getSaveFiles(self):
        '''Get the save file names'''
        self.files = []
        for file in os.listdir(self.data_file_path):
            if file.endswith(".inventory"):
                self.files.append(file)

        self.logDebug(self.files)

        return self.files

    def getObjects(self):
        for ID in Inventory.objs:
            log = f'{Inventory.objs[ID].description} has grid: {Inventory.objs[ID].grid}'
            self.logDebug(log)

    def getStat(self,
                inventory_count=False,
                value=False,
                weight=False,
                tags=False
                ):
        '''Return information about the inventory as a string'''

        if inventory_count == True:
            return 'Needs attention'

        elif value == True:
            value = 0
            for key in Inventory.objs:
                value += Inventory.objs[key].getValue()
            return f"${format(int(value), ',.0f')}"

        elif weight == True:
            weight = 0
            for key in Inventory.objs:
                weight += Inventory.objs[key].getWeight()
            return f"{format(int(weight), ',.0f')} lbs"

        elif tags == True:
            return Inventory.getTopTags()

        else:
            self.logError('No flags were set to True')
            return 'Error'

    def loadData(self):
        '''Load the user's data from any non-encrypted save file.  Changes
           self._inventory'''
        if self.data_was_loaded == True:
            return

        self.logDebug(f'Loading {self.user_file}')

        # Catch errors if the file doesn't exist
        try:
            # Open the file in read mode with utf-8 encoding
            with open(self.user_file, 'r', encoding='utf-8') as f:
                # Load the data as a dictionary
                self._inventory = json.load(f)
                # self.logInfo(f'loaded data:\n{json.dumps(inventory, indent=4)}')

        except FileNotFoundError:
            try:
                with open(self.data_file_path + self.user_file) as f:
                    # Load the data as a dictionary
                    self._inventory = json.load(f)
                    # self.logDebug(f'loaded data:\n{json.dumps(inventory, indent=4)}')
            except FileNotFoundError:
                # If the load data is None, set the data to its default
                self.logError(f'{self.user_file} not found')

        if self._inventory == None:
            return False

    def loadDataEncrypted(self):
        '''Load the user's data from an encrypted save file. Changes
           self._inventory'''
        returned_data = self.sec.decryptFile(self.user_file)
        if returned_data == None:
            return False
        elif isinstance(returned_data, dict):
            self._inventory = returned_data
            self.user_file_en
            return True
        else:
            self.logError(f'Was expecting False or dict type. Got: {isinstance(returned_data)}')
            return False

    def loadSettings(self):
        '''Load the settings file'''
        try:
            with open(self.data_file_path + '.user_settings', 'r') as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            with open(self.data_file_path + '.user_settings', 'w') as f:
                json.dump(self.default_settings, f, ensure_ascii=False, indent=4)
            self.settings = self.default_settings


    def restart(self):
        '''Reset the app to the load file screen. Save user data to disk and remove data from memory'''
        # Save user data
        self._saveData()
        # Remove user data from memory
        self._cleanup()
        # Create new widgets and start at the home screen
        self._setup()

    def start(self, file_name, encrypted=False):
        self.user_file = file_name

        if encrypted == False:
            self.loadData()
        else:
            if self.loadDataEncrypted() == False:
                return False

        self.createUserScreens()
        self._setupExistingInventory()
        self.changeScreen('inventory')
        self.changeScreen('0')

    def select(self, selection):
        '''Set the selected object directly or by using the ID.
           Select nothing by passing None as the argument.'''

        if selection == None:
            self.selected = None
            Inventory.selected.deselect()
        elif isinstance(selection, Inventory):
            self.selected = selection
            Inventory.selected = selection
        else:
            self.selected = Inventory.getByID(selection)
            Inventory.selected = self.selected
            self.logInfo(f'Selected {self.selected}')

        self.logDebug(f'SELECTED: {self.selected}')

    def updateInventoryData(self, popup):
        '''Update an inventory item's data from user input'''
        self.logDebug('Updating inventory data')
        popup.inventory.description = popup.description.text
        popup.inventory.usd_value = popup.usd_value.text
        popup.inventory.weight = popup.weight.text
        popup.inventory.addTags(popup.tags.text)
        popup.inventory.widget.assignValues()
        Inventory.getByID(popup.inventory.container).widget.assignValues()

    def _cleanup(self):
        '''Remove the inventory that was loaded previously'''
        self.user_file = None
        self.is_new_inventory = False
        self.sec.reset()
        Inventory.cleanup()
        self.selection.cleanup()

        while len(self.app_sm.screens) > 0:
           self.app_sm.remove_widget(self.app_sm.screens[0])

        self.data_was_loaded = False
        self.user_file_en = False
        Inventory.resetChangeMade()

    def _saveData(self):
        '''Save data if necessary'''

        if self.inventory.wasChangeMade() == True:
            self.logDebug('Changes were made. Getting save data')
            data = Inventory.getSaveData()

            self.logDebug('Saving JSON data to file')

            # Add necessary file naming conventions
            if self.user_file_en == True:
                if self.user_file[0:2] != 'e.':
                    self.user_file = 'e.' + self.user_file
            if '.inventory' not in self.user_file:
                self.user_file += '.inventory'
            if self.data_file_path not in self.user_file:
                self.user_file = self.data_file_path + self.user_file

            # If the file is encrypted save it encrypted
            if self.user_file_en == True:
                self.sec.encryptFile(self.user_file, data)
            # If the file isn't encrypted save it without encryption
            else:
                with open(self.user_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)
        else:
            self.logInfo('No changes made. Skipping save')

    def _setupExistingInventory(self):
        '''Use the loaded data to create the inventory data and objects'''
        data = self._inventory

        for key in data:
            data[key]['ID'] = int(key)
            self.createInventoryObject(data[key])

        self.data_was_loaded = True

        # Reset the Inventory._changes_made attribute to False to avoid saving the same data
        Inventory.resetChangeMade()
        # Inventory.checkLoad()
