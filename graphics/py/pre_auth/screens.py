import pprint

# from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

from resources.utilities import UtilityMethods, LogMethods


class LoginScreen(Screen, UtilityMethods, LogMethods):
    ''' The window that draws necesary widgets to the screen such as buttons, text inputs,
        and labels. It inherits from kivy.uix.screenmanager.screen.Screen. It also does
        the following:
            - Grabs widgets from the .kv file for access within this class
            - Check for tab and enter presses on the keyboard
            - handle button presses
            - call appropriate functions if buttons are pressed'''

    # Capture the TextInput widgets from main_widgets.kv LoginWindow class
    account = ObjectProperty(None)
    pswd = ObjectProperty(None)

    def __init__(self, **kwargs):
        '''Call WindowKeyboard.__init__() with super().__init__().  Assign other
           instance variables.'''

        # Allows us to call our own LoginScreen.__init__() without overriding Kivy's Screen.__init__()
        super(LoginScreen, self).__init__(**kwargs)

        # # Allow me to check if the enter key is pressed
        # Window.bind(on_key_down=self._on_keyboard_down)

        self.__initLog__(
            file_str='pre_auth_screens',
            class_str='LoginScreen'
        )

        # Put Kivy widgets into a dictionary for looping/DNRY methods in UtilityMethods class
        self.widgets = {
            'TextInputs': {}
        }
        self.widgets['TextInputs']['account'] = self.account
        self.widgets['TextInputs']['pswd'] = self.pswd
        self.logDebug('KvLogic', f'self.widgets was created:\n{pprint.pformat(self.widgets, indent=4)}')

    def _authenticate(self):
        '''Check if the user input is valid.  Call the database function to check
           if the user exists.'''
        if self.widgets['TextInputs']['account'].text != '' and \
           self.widgets['TextInputs']['pswd'].text != '':
            self.logInfo('AUTH', f'self._authenticate CONFIRMED {self.account.text}!')
            return True
        else:
            self.logInfo('AUTH', f'self._authenticate DENIED {self.account.text}!')
            return False

    def initDefaultPopupText(self):
        '''Set the default popup text messages, popup button prompt, and popup title.  Must be done
           after the app is instantiated so we can access app.settings.'''

        self.popup_text = {}
        self.popup_text['messages'] = {
            'invalid login': 'Invalid username/email or password.',
            'blank login': 'Please provide a username/email and password.',
            'footer': 'Please check and try again.'
        }
        self.popup_text['button'] = 'Try again'
        self.popup_text['title'] = 'Invalid Login'

        log = f'Init\'d self.popup_text dictionary:\n{pprint.pformat(self.popup_text, indent=4)}'
        self.logDebug('App', log)


class CreateAccountScreen(Screen, UtilityMethods, LogMethods):
    ''' The window that draws necesary widgets to the screen such as buttons, text inputs,
        and labels. It inherits from kivy.uix.screenmanager.screen.Screen. It also does
        the following:
            - Grabs widgets from the .kv file for access within this class
            - Check for tab and enter presses on the keyboard
            - handle button presses
            - call appropriate functions if buttons are pressed'''

    username = ObjectProperty(None)
    email = ObjectProperty(None)
    pswd = ObjectProperty(None)
    pswdrpt = ObjectProperty(None)

    def __init__(self, **kwargs):
        # Allows us to call our own CreateAccountScreen.__init__() without overriding
        # Kivy's Screen.__init__()
        super(CreateAccountScreen, self).__init__(**kwargs)

        # # Allow me to check if the enter key is pressed
        # Window.bind(on_key_down=self._on_keyboard_down)

        # Creates self.log which saves to app_home_dir/logs/inventory.day.month.year.log
        self.__initLog__(
            file_str='pre_auth_screens',
            class_str='CreateAccountScreen'
        )

        # Put the Kivy widgets into a dictionary for DNRY/ looping
        self.widgets = {
            'TextInputs': {
                'pswd': self.pswd,
                'pswdrpt': self.pswdrpt,
                'email': self.email,
                'username': self.username
            }
        }
        self.logDebug('KvLogic', f'Created self.widgets:\n{pprint.pformat(self.widgets, indent=4)}')

    def _authenticate(self):
        '''Check if the user input is valid.  Call the database function to check
           if the user exists.'''
        if self.username.text != '' and \
           self.email.text != '' and \
           self.pswd.text != '' and \
           self.pswdrpt.text != '':
            self.logInfo('AUTH', f'self._authenticate CONFIRMED {self.username.text}!')
            return True
        else:
            self.logInfo('AUTH', f'self._authenticate DENIED {self.username.text}!')
            return False

    def initDefaultPopupText(self):
        '''Set the default popup text messages, popup button prompt, and popup title.  Must be done
           after the app is instantiated so we can access app.settings.'''
        self.popup_text = {
            'messages': {
                'invalid username length': 'Username should be at least ' +
                                           f'{self.manager.app.settings["username min length"]} ' +
                'characters long',
                'invalid email': 'The email must be a properly formatted email.',
                'password mismatch': 'The passwords do not match.',
                'password length': f'Your password must be at least ' +
                f'{self.manager.app.settings["password min length"]} characters long',
                'footer': 'Please try again.'
            },
            'button': 'Try again',
            'title': 'Invalid Account Creation Attempt'
        }
        self.logDebug(
            'App',
            f'Init\'d self.popup_text dictionary:\n{pprint.pformat(self.popup_text, indent=4)}'
        )


class InventoryScreenManager(ScreenManager, LogMethods):
    '''Handles screen changes and holds screen widgets in self.get_current, self.get_screen('name')'''

    def __init__(self, **kwargs):
        super(InventoryScreenManager, self).__init__(**kwargs)
        self.__initLog__(
            file_str='pre_auth_screens',
            class_str='InventoryScreenManager'
        )
        self.logDebug('KvOps', 'Instantiated an InventoryScreenManager')
