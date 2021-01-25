from pprint import pformat

from kivy.config import Config
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import NoTransition, SlideTransition

from graphics.screens import LoadFileScreen, CreateFileScreen
from graphics.screens import InventoryScreenManager
from graphics.datagrid import DataGrid, ContainerHeadingRow
from resources.kv_extensions import KivyExtensions
from resources.datahandler import DataHandler
from resources.inventoryobjects import InventoryObject
from resources.utilities import LogMethods, Security
from resources.selection import Selection


# Without this, right clicking will leave a red circle behind
Config.set('input', 'mouse', 'mouse, multitouch_on_demand')


class MyInventoryApp(App, KivyExtensions, DataHandler, LogMethods):

    def __init__(self, **kwargs):
        super(MyInventoryApp, self).__init__(**kwargs)
        self.__initLog__(file_str='inventory', class_str='MyInventoryApp')
        # Allow access to the Selection class through the app instance
        self.selection = Selection
        self.data_file_path = 'save_data/'

        self.loadSettings()

        self.logInfo(f'Started session with settings:\n{pformat(self.settings, indent=4)}')

        # Set window color:  black: (0, 0, 0, 1), white: (1, 1, 1, 1)
        Window.clearcolor = (0.06, 0.06, 0.06, 1)

        # Load the .kv files to start building the GUI
        for file in self.settings['startup kv files']:
            Builder.load_file(file)

        self.logDebug(f'Used kivy.lang.Builder to load files {self.settings["startup kv files"]}')

        # Allow children of the WindowManager instance to access self.settings in the App instance
        InventoryScreenManager.app = self

        # Create a ScreenManager instance with no transition movement
        self.sm = InventoryScreenManager(transition=NoTransition())
        log = 'Created self.sm, instance of InventoryScreenManager'
        self.logDebug(log)

        self.user_file_en = False
        self.sec = Security(self)
        self._setup()

    def _setup(self):
        # name='name' allows the screen manager to change screens using self.current='screen'
        # name can also be defined in the kv/main_widgets.kv file using "name: 'load file'" under
        # class declaration
        lfs = LoadFileScreen(self, name='load file')
        cfs = CreateFileScreen(self, name='create file')
        screens = [lfs, cfs]

        # Make sure sm knows how to handle changes to self.current
        # such as self.current = 'account screen'
        for screen in screens:
            self.sm.add_widget(screen)

        lfs.fillFileOptions()

        # Set the current screen
        self.sm.current = 'load file'
        self.sm.transition = NoTransition()

    def build(self):
        '''Without returning self.sm (ScreenManager), the app would be a blank screen.'''
        self.logDebug('self.build called. building...')
        self.title = 'My Inventory'
        return self.sm

    def on_stop(self):
        '''Execute this function when the application is closed'''
        self.logInfo(f'changes_made = {self.inventoryobject.wasChangeMade()}')
        if self.inventoryobject.wasChangeMade() == True:
            try:
                log = 'Attempting to save inventory..'
                self.logInfo(log)
                self._saveData()
                self.logInfo('Save succeeded')
            except AttributeError:
                self.logError('Save failed!')
        self.logInfo('Exiting the application')


if __name__ == '__main__':
    # Start the application
    app = MyInventoryApp()
    app.run()
