import pprint

# from kivy.core.window import Window
# from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from resources.utilities import UtilityMethods, WindowKeyboard, LogMethods


class AccountOverviewScreen(Screen, WindowKeyboard, UtilityMethods, LogMethods):

    parent_layout = ObjectProperty(None)
    data_grid = ObjectProperty(None)

    def __init__(self, **kwargs):
        # Allows us to call our own AccountOverviewScreen.__init__() without overriding Kivy's Screen.__init__()
        super(AccountOverviewScreen, self).__init__(**kwargs)
        # Creates self.log which saves to app_home_dir/logs/inventory.day.month.year.log
        self.__initLog__(
            file_str='account_screens',
            class_str='AccountOverviewScreen'
        )

        self.logInfo('kv_ops', 'Creating an AccountOverviewScreen instance..')

        # Put input widgets here so we can grab the user input at some point
        self.widgets = {
            'TextInputs': {}
        }

        # Make sure the data_grid knows what format to follow
        self.data_grid.setObjectCategory('containers')

        self.logInfo('kv_ops', 'Calling self.data_grid.TextRandomPopulate..')

        # Test the rows with random data
        self.data_grid.TestRandomPopulate()

    def initDefaultPopupText(self):
        '''Set the default text to be displayed in certain situations'''


class ContainerOverviewScreen(Screen, WindowKeyboard, UtilityMethods, LogMethods):

    parent_layout = ObjectProperty(None)
    data_grid = ObjectProperty(None)

    def __init__(self, **kwargs):
        # Allows us to call our own AccountOverviewScreen.__init__() without overriding Kivy's Screen.__init__()
        super(ContainerOverviewScreen, self).__init__(**kwargs)
        # Creates self.log which saves to app_home_dir/logs/inventory.day.month.year.log
        self.__initLog__(
            file_str='account_screens',
            class_str='ContainerOverviewScreen'
        )

        self.logInfo('kv_ops', 'Creating a ContainerOverviewScreen instance..')

        # Put input widgets here so we can grab the user input at some point
        self.widgets = {
            'TextInputs': {}
        }

        # Make sure the data_grid knows what format to follow
        self.data_grid.setObjectCategory('things')

        self.logInfo('kv_ops', 'Calling self.data_grid.TextRandomPopulate..')

        # Test the rows with random data
        self.data_grid.TestRandomPopulate()

    def initDefaultPopupText(self):
        '''Set the default text to be displayed in certain situations'''


class ThingOverviewScreen(Screen, WindowKeyboard, UtilityMethods, LogMethods):
    pass
