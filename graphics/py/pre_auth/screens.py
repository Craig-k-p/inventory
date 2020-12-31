import pprint

from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

from resources.utilities import UtilityMethods, LogMethods


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


class LoadFileScreen(Screen, UtilityMethods, LogMethods):
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


class CreateFileScreen(Screen, UtilityMethods, LogMethods):
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
