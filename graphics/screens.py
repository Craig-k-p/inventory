import pprint

from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button

from graphics.thing_view import ThingView
from graphics.toolbar import Toolbar
from resources.utilities import LogMethods


class CenterAnchorLayout(AnchorLayout):
    '''FileButton class declared in screens.kv'''


class FileButton(Button, LogMethods):
    '''FileButton class declared in screens.kv'''
    app = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(FileButton, self).__init__(**kwargs)
        self.__initLog__(file_str='screens.py', class_str='FileButton')

    def selectFile(self):
        self.app.user_file = self.file
        self.logDebug(self.file)
        self.app.createUserScreens()


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
            b.file = file
            on_release = b.selectFile
            layout.add_widget(b)
            self.file_button_parent.add_widget(layout)
            self.logDebug(f'Added {file} button')


class CreateFileScreen(Screen, LogMethods):
    ''' The screen that draws necesary widgets to the window such as buttons, text inputs,
        and labels. It inherits from kivy.uix.screenmanager.screen.Screen'''

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
        if self.app.doesFileExist(file_name) == True:
            errors.append('File already exists')
            self.file_name_input.error = True
            self.error += 1
        else:
            self.file_name_input.error = False

        # Add this error if the file contains anything other than underscors and alphanumeric
        # characters
        if file_name.replace('_','').isalnum() == False:
            errors.append('Only alphanumeric characters and underscores allowed.')
            self.file_name_input.error = True
            self.error += 1
        else:
            self.file_name_input.error = False

        # If there are no errors, set the user_file name and load/present the user's data
        if self.error == 0:
            self.logDebug('No errors found')
            self.app.user_file = file_name
            self.app.createUserScreens()
        # If there are errors, log them and create a popup to warn the user
        else:
            for error in errors:
                self.logDebug(error)
            self.app.createPopup(errors=errors)
            return


class InventoryScreenManager(ScreenManager, LogMethods):
    '''Handles screen changes and holds screen widgets in self.get_current,
       self.get_screen('name')'''

    def __init__(self, **kwargs):
        super(InventoryScreenManager, self).__init__(**kwargs)
        self.__initLog__(file_str='pre_auth_screens', class_str='InventoryScreenManager')


class AccountOverviewScreen(Screen, LogMethods):

    parent_layout = ObjectProperty(None)
    data_grid = ObjectProperty(None)
    app = ObjectProperty(None)
    toolbar = ObjectProperty(None)

    def __init__(self, app, **kwargs):
        # Allows us to call our own AccountOverviewScreen.__init__() without overriding Kivy's Screen.__init__()
        super(AccountOverviewScreen, self).__init__(**kwargs)
        self.app = app
        self.__initLog__(file_str='screens.py', class_str='AccountOverviewScreen')

        # Make sure the data_grid knows what format to follow
        self.data_grid.setDataGridObjectType('container')

        # Fill the user data into rows
        self.data_grid.fillUserData(self.app)

        self.toolbar.search.bind(text=app.inventoryobject.applySearch)


class ContainerOverviewScreen(Screen, LogMethods):
    '''Overview of all containers in the user's inventory'''

    parent_layout = ObjectProperty(None)
    data_grid = ObjectProperty(None)
    app = ObjectProperty(None)

    def __init__(self, app, **kwargs):
        # Allows us to call our own AccountOverviewScreen.__init__() without overriding Kivy's Screen.__init__()
        super(ContainerOverviewScreen, self).__init__(**kwargs)
        self.app = app
        self.__initLog__(file_str='screens.py', class_str='ContainerOverviewScreen')

        # Make sure the data_grid knows what format to follow
        self.data_grid.setDataGridObjectType('thing')

        # Fill the user data into rows
        self.data_grid.fillUserData(self.app)

        self.toolbar.search.bind(text=app.inventoryobject.applySearch)
