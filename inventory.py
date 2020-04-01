'''
https://www.youtube.com/watch?v=xaYn4XdieCs

Create executable that can be pinned to Start or Task bar:

Resource:
https://winaero.com/blog/pin-a-batch-file-to-the-start-menu-or-taskbar-in-windows-10/

Create a .bat file with commands:
    python full_path_to_file
    cmd /k

Create a shortcut for the .bat file
Right click and edit target to say:
    cmd /k already_existing_filepath_that_you_should_not_edit

Voilla!

'''
from pprint import pformat

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import NoTransition, SlideTransition

from graphics.py.pre_auth.screens import LoginScreen, CreateAccountScreen, InventoryScreenManager
from graphics.py.account.datagrid import DataGrid, ContainerHeadingRow
from resources.kv_extensions import KivyExtensions
from resources.inventoryhandler import InventoryHandler
from resources.utilities import LogMethods


class MyInventoryApp(App, KivyExtensions, InventoryHandler, LogMethods):

    # Unique ID for each of the user's objects
    uid_counter = 0

    def __init__(self, **kwargs):
        super(MyInventoryApp, self).__init__(**kwargs)
        self.__initLog__(
            file_str='inventory',
            class_str='MyInventoryApp'
        )

        self.logInfo('Creating MyInventoryApp instance')

        # Set window to white
        Window.clearcolor = (0, 0, 0, 1)

        self.popup_errors = []
        self.settings = {
            'password min length': 0,
            'username min length': 0,
            'start screen': 'login', # account, container, thing
            'startup transition': NoTransition(),
            'app transition type': SlideTransition(),
            'save file': 'save_data/save_data',
            'backup save file': 'save_data/backup_save_data',
            'log filtering': 'InventoryHandler.py' }
        self.kv_settings = {
            'startup kv files': ['graphics/kv/pre_auth/screens.kv', 'graphics/kv/account/screens.kv'],
            'kv popup file': 'graphics/kv/pre_auth/popups.kv',
            'overview options button size_hint': (None, 1),
            'overview options button width': 35,
            'overview weight field width': 60,
            'popup auto_dismiss': False,
            'popup required fields': ['description', 'usd_value', 'weight'],
            'popup size_hint': (.75, .75),
            'standard font': 'arial',
            'text color': (1, 1, 1, 1),
            'title font name': 'segoesc',}
        self.validations = {
            'allowed button calls': (
                'changeScreen',
                'createAccount',
                'login',
                'createThingPopup',
                'createContainerPopup',
                'createInventoryObject'
            ),
            'authentication needed': {
                'account': False,
                'container': False,
                'thing': False,
                'login': False,
                'create account': False}}

        self.logInfo(f'Started session with settings:\n{pformat(self.settings, indent=4)}')
        self.logInfo(f'Started session with settings:\n{pformat(self.kv_settings, indent=4)}')
        log = f'Started session with validations:\n{pformat(self.validations, indent=4)}'
        self.logInfo(log)

        # Load the .kv files to start building the GUI
        for file in self.kv_settings['startup kv files']:
            Builder.load_file(file)

        self.logDebug(f'Used kivy.lang.Builder to load files {self.kv_settings["startup kv files"]}')

        # Create a ScreenManager instance with no transition movement
        self.sm = InventoryScreenManager(transition=self.settings['startup transition'])
        log = 'Created self.sm, instance of InventoryScreenManager with startup transition as '
        log += f'{self.settings["startup transition"]} --- {self.sm}'
        self.logDebug(log)

        # Allow children of the WindowManager instance to access self.settings in the App instance
        self.sm.app = self

        # Create a separate function to handle logging out and in, so no data is accidently preserved on a screen.
        screens = [
            # These are added to the screen manager sm so that the screen manager sm
            # knows which screens we are refering to  (<-- better wording needed)
            # name='name' allows the screen manager to change screens using self.current='screen'
            CreateAccountScreen(name='create account'),
            LoginScreen(name='login'),
            # name can also be defined in the kv/main_widgets.kv file using "name: 'account window'" under
            # class declaration
        ]

        log = f'Created login, account, and create account screens with "screens" var: '
        log += f'{pformat(screens, indent=4)}'
        self.logDebug(log)

        # Make sure sm knows how to handle changes to self.current
        # such as self.current = 'account window'
        for screen in screens:
            self.sm.add_widget(screen)
        self.logDebug('Added the screens to self.sm InventoryScreenManager instance')

        # Set the current screen to login window
        self.sm.current = self.settings['start screen']
        self.sm.transition = self.settings['app transition type']
        self.logDebug('Set the first screen to settings["start screen"]')

    def build(self):
        '''Without returning self.sm, the app would be a blank screen.'''
        self.logDebug('self.build called')
        self.title = 'My Inventory'
        return self.sm

    def on_stop(self):
        '''Execute this function when the application is exited'''
        self.logDebug('Saving data...')
        # Save the user data to a file if necessary
        self.saveData()
        self.logDebug('Exiting the application..')


if __name__ == '__main__':
    # Start the application
    app = MyInventoryApp()
    app.run()
