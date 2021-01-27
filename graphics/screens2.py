import pprint

from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button

from graphics.toolbar2 import Toolbar
from resources.utilities import LogMethods


from json import dumps

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from resources.utilities import LogMethods
# from resources.inventory import Inventory
from graphics.row2 import HeadingRow, DataRow


class DataGrid(GridLayout, LogMethods):
    app = ObjectProperty(None)

    def __init__(self, **kwargs):
        '''Creates the widgets in a user-defined manner'''
        # Init the parent, ScrollView
        super(DataGrid, self).__init__(**kwargs)
        self.__initLog__(file_str='datagrid.py', class_str='DataGrid')
        self.clicked = None

    def __repr__(self):
        s = f'<DataGrid object with parent: >'
        return s

    def on_touch_down(self, touch):
        '''This allows me to get click/touch coordinates from the user. Without calling
           the super method, buttons and other UI elements don't respond to clicks.'''

        self.logDebug(f'\nClick-{touch.pos}')
        super().on_touch_down(touch)
        self.app.inventory.setBounds(self, touch)

        row_clicked = False
        # Check which widget was clicked
        # For each widget in self.children
        for widget in self.children:

            # Check if it is a DataRow instance rather than a heading row
            if isinstance(widget, DataRow):
                was_clicked = widget.wasClicked(touch)

                if was_clicked == True:
                    row_clicked = True
                    self.app.selection(widget.inventory)

                    # Check for a double-click
                    if touch.is_double_tap:
                        self.logDebug(f'Double-click detected')

                        # If inventory with contents is double-clicked, change screen
                        if isinstance(widget, DataRow) and widget.inventory.hasContents() == True:
                            self.app.changeScreen(widget.inventory.ID)
                            self.app.selection(None)
                        # If a thing is selected, pass
                        elif isinstance(widget, DataRow) and widget.inventory.hasContents() == False:
                            pass
                        else:   # Empty space clicked.  Deselect
                            self.app.selection(None)

        if row_clicked == False:
            self.app.selection(None)

        self.app.app_sm.current_screen.toolbar.presentOptions()

    def addDataRow(self, inventory):
        '''Add a row of fields to the GridLayout with the given data
           data is a dict of user input'''

        # Add the datagrid to the widget
        if inventory.parent_widget == None:
            inventory.parent_widget = self

        # Instantiate a data row with ID and data
        new_row = DataRow(inventory)

        inventory.widget = new_row

        self.logDebug(f'Adding a row for the {new_row.object.description} to the grid')
        self.add_widget(new_row)

    def deleteObject(self):
        '''Delete an object and its row from the GridLayout in the DataGrid'''
        # Delete the inventory object and its data
        selection = self.app.selection.get().getObj()
        if selection.hasContents() == True:
            self.logDebug(f'{selection} has contents. Warning user.')
            self.app.createPopup(warn=True)
        else:
            selection.delete()

    def fillUserData(self, app):
        '''Populate the data rows with user data during application startup'''
        self.logDebug(f'Filling the DataGrid with objects')

        # # Get access to the application instance
        # if self.app == None:
        #     self.app = app

        self.app.inventory.updateWidgets(self)


class CenterAnchorLayout(AnchorLayout):
    '''FileButton class declared in screens.kv'''


class FileButton(Button, LogMethods):
    '''FileButton class declared in screens.kv'''
    app = ObjectProperty(None)
    prompt = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(FileButton, self).__init__(**kwargs)
        self.__initLog__(file_str='screens.py', class_str='FileButton')

    def selectFile(self):
        if self.text[0:2] == 'e.':
            self.app.createPopup(prompt_password=True, file=self.user_file)
        else:
            self.app.start(self.user_file)


class LoadFileScreen(Screen, LogMethods):
    ''' The window that draws necesary widgets to the screen such as buttons, text inputs,
        and labels. It inherits from kivy.uix.screenmanager.screen.Screen'''

    file_button_parent = ObjectProperty(None)

    def __init__(self, app, **kwargs):
        super(LoadFileScreen, self).__init__(**kwargs)
        self.__initLog__(file_str='screens.py', class_str='LoadFileScreen')
        self.app = app

    def fillFileOptions(self):
        '''Find the inventories and fill them into the file_button_parent widget so the user
           can select one'''

        files = self.parent.app.getSaveFiles()

        for file in files:
            layout = CenterAnchorLayout()
            b = FileButton(text=file)
            b.on_release = b.selectFile
            b.user_file = file
            on_release = b.selectFile
            layout.add_widget(b)
            self.file_button_parent.add_widget(layout)
            self.logDebug(f'Added {file} button')


class CreateFileScreen(Screen, LogMethods):
    ''' The screen that draws necesary widgets to the window such as buttons, text inputs,
        and labels. It inherits from kivy.uix.screenmanager.screen.Screen'''

    encrypted_checkbox = ObjectProperty(None)
    file_name_input = ObjectProperty(None)

    def __init__(self, app, **kwargs):
        super(CreateFileScreen, self).__init__(**kwargs)
        self.__initLog__(file_str='pre_auth_screens', class_str='CreateFileScreen')
        file_name_input = ObjectProperty(None)
        self.app = app

    def checkUserInputFormat(self):
        '''Check if the user input is valid'''
        file_name = self.file_name_input.text.lower().strip()

        self.error = 0

        errors = []

        # Add this error if the filename is too short
        if len(file_name) < 1:
            errors.append('File name is blank')
            self.file_name_input.error = True
            self.error += 1
        else:
            self.file_name_input.error = False

        # Add this error if the file already exists
        if self.app.doesFileExist(file_name, self.encrypted_checkbox.active) == True:
            errors.append('File already exists')
            self.file_name_input.error = True
            self.error += 1
        else:
            self.file_name_input.error = False

        # Add this error if the file contains anything other than underscors and alphanumeric
        # characters
        if file_name.replace('_','').isalnum() == False:
            errors.append('Only alphanumeric characters')
            errors.append('and underscores are allowed.')
            self.file_name_input.error = True
            self.error += 1
        else:
            self.file_name_input.error = False

        # If there are no errors, set the user_file name and load/present the user's data
        if self.error == 0:
            self.logDebug('No errors found')
            self.app.user_file = file_name
            # If the user indicated that they want the file to be encrypted
            if self.encrypted_checkbox.active == True:
                self.logInfo(f'User wants to encrypt {file_name}.inventory')
                self.app.createPopup(create_password=True)
            else:
                self.app.createUserScreens()
                self.app.is_new_inventory = True
        # If there are errors, log them and create a popup to warn the user
        else:
            for error in errors:
                self.logDebug(error)
            self.app.createPopup(errors=errors)
            return


class InventoryOverviewScreen(Screen, LogMethods):
    parent_layout = ObjectProperty(None)
    app = ObjectProperty(None)
    toolbar = ObjectProperty(None)

    def __init__(self, app, **kwargs):
        # Allows us to call our own AccountOverviewScreen.__init__() without overriding Kivy's Screen.__init__()
        super(InventoryOverviewScreen, self).__init__(**kwargs)
        self.app = app
        self.__initLog__(file_str='screens.py', class_str='InventoryOverviewScreen')

        self.toolbar.search.bind(text=app.inventory.applySearch)


class InventoryScreen(Screen, LogMethods):
    '''Overview of all containers in the user's inventory'''
    data_grid = ObjectProperty(None)
    app = ObjectProperty(None)
    # screens = []

    def __init__(self, **kwargs):
        super(InventoryScreen, self).__init__(**kwargs)
        self.__initLog__(file_str='screens.py', class_str='InventoryScreen')

        # InventoryScreen.screens.append(self.name)

        self.logDebug('Screen created')

        # Fill the user data into rows
        # self.data_grid2.fillUserData(self.app)

    # def __repr__(self):
    #     return f'<InventoryScreen object of {self.invobj}>'

    def delete(self):
        InventoryScreen.screens.remove(self.name)
