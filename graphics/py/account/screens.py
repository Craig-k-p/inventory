import pprint

from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from graphics.py.account.thing_view import ThingView
from graphics.py.account.toolbar import Toolbar
from resources.utilities import UtilityMethods, LogMethods


class AccountOverviewScreen(Screen, UtilityMethods, LogMethods):

    parent_layout = ObjectProperty(None)
    data_grid = ObjectProperty(None)
    miapp = ObjectProperty(None)

    def __init__(self, **kwargs):
        # Allows us to call our own AccountOverviewScreen.__init__() without overriding Kivy's Screen.__init__()
        super(AccountOverviewScreen, self).__init__(**kwargs)

        # # Allow me to check if the enter key is pressed
        # Window.bind(on_key_down=self._on_keyboard_down)

        # Creates a logger for the current class
        self.__initLog__(
            file_str='account_screens',
            class_str='AccountOverviewScreen'
        )

        self.logInfo('kv Ops', 'Creating an AccountOverviewScreen instance..')

        # Put input widgets here so we can grab the user input at some point
        self.widgets = {
            'TextInputs': {}
        }

        # Make sure the data_grid knows what format to follow
        self.data_grid.setDataGridObjectType('container')

        self.logInfo('kv Ops', 'Calling self.data_grid.fillUserData')

        # Fill the user data into rows
        self.data_grid.fillUserData(self.miapp)

    def initDefaultPopupText(self):
        '''Set the default text to be displayed in certain situations'''

    def buttonPress(self):
        self.logInfo('kv Ops', 'Enter pressed in AccountOverviewScreen!')


class ContainerOverviewScreen(Screen, LogMethods):
    '''Overview of all containers in the user's inventory'''

    parent_layout = ObjectProperty(None)
    data_grid = ObjectProperty(None)
    miapp = ObjectProperty(None)

    def __init__(self, **kwargs):
        # Allows us to call our own AccountOverviewScreen.__init__() without overriding Kivy's Screen.__init__()
        super(ContainerOverviewScreen, self).__init__(**kwargs)

        # # Allow me to check if the enter key is pressed
        # Window.bind(on_key_down=self._on_keyboard_down)

        # Creates a logger for the current class
        self.__initLog__(
            file_str='account_screens',
            class_str='ContainerOverviewScreen'
        )

        self.logInfo('kv Ops', 'Creating a ContainerOverviewScreen instance..')

        # Put input widgets here so we can grab the user input at some point
        self.widgets = {
            'TextInputs': {}
        }

        # Make sure the data_grid knows what format to follow
        self.data_grid.setDataGridObjectType('thing')

        self.logInfo('kv Ops', 'Calling self.data_grid.fillUserData')

        # Fill the user data into rows
        self.data_grid.fillUserData(self.miapp)

    def initDefaultPopupText(self):
        '''Set the default text to be displayed in certain situations'''

    def buttonPress(self):
        self.logInfo('kv Ops', 'Enter pressed in ContainerOverviewScreen!')


class ThingOverviewScreen(Screen, UtilityMethods, LogMethods):
    thing_view = ObjectProperty(None)

    def __init__(self, **kwargs):
        # Allows us to call our own AccountOverviewScreen.__init__() without overriding Kivy's Screen.__init__()
        super(ThingOverviewScreen, self).__init__(**kwargs)

        # # Allow me to check if the enter key is pressed
        # Window.bind(on_key_down=self._on_keyboard_down)

        # Creates a logger for the current class
        self.__initLog__(
            file_str='screens.py',
            class_str='AccountOverviewScreen'
        )

        self.logInfo('kv Ops', 'Creating an ThingOverviewScreen instance..')

        # Put input widgets here so we can grab the user input at some point
        self.widgets = {
            'TextInputs': {}
        }

    def buttonPress(self):
        self.logInfo('kv Ops', 'Enter pressed in ThingOverviewScreen!')
