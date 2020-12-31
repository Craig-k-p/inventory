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
    app = ObjectProperty(None)
    toolbar = ObjectProperty(None)

    def __init__(self, app, **kwargs):
        # Allows us to call our own AccountOverviewScreen.__init__() without overriding Kivy's Screen.__init__()
        super(AccountOverviewScreen, self).__init__(**kwargs)
        self.app = app
        self.__initLog__(file_str='account_screens', class_str='AccountOverviewScreen')

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
        self.__initLog__(file_str='account_screens', class_str='ContainerOverviewScreen')

        # Make sure the data_grid knows what format to follow
        self.data_grid.setDataGridObjectType('thing')

        # Fill the user data into rows
        self.data_grid.fillUserData(self.app)

        self.toolbar.search.bind(text=app.inventoryobject.applySearch)
