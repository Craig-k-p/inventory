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
        self.widgets = {
            'TextInputs': {}
        }
        self.logDebug('KvLogic', f'Created AccountOverviewScreen instance')

    def initDefaultPopupText(self):
        '''Set the default text to be displayed in certain situations'''

    def initLog(self):
        self.__initLog__(
            file_str='account_screens',
            class_str='AccountOverviewScreen'
        )


class BoxOverviewScreen(Screen, WindowKeyboard, UtilityMethods, LogMethods):
    pass


class ThingOverviewScreen(Screen, WindowKeyboard, UtilityMethods, LogMethods):
    pass
