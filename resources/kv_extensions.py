import pprint

from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
# from kivy.graphics.context_instructions import Color
# from kivy.graphics.vertex_instructions import Rectangle

from graphics.py.pre_auth.popup import PopupContent


class KivyExtensions():
    '''Used to separate the Kivy graphics methods needed in MyInventoryApp
       from the MongoEngine database methods needed for the back end.'''

    def _clearPopupErrors(self):
        self.popup_errors = []

    def createPopup(self):
        '''Method that does the following:
            -Load the kv file that defines what goes into the popup
            -Create an instance of Popup
            -Set the text for the label and button
            -Draw the popup to the screen
            -Unload the file to avoid errors.'''

        # Get the current screen
        current_screen = self.sm.current_screen

        # Create the text messages necessary for the popup found in kv_screens.py
        current_screen.initDefaultPopupText()

        # Get the screen's popup text dictionary for screen-specific popup messages
        text = current_screen.popup_text

        # Load the popup content from file and create an instance of PopupContent
        Builder.load_file(self.kv_settings['kv popup file'])
        self.logDebug('KvLogic', f'kivy.lang.Builder loaded the file {self.kv_settings["kv popup file"]}')

        # Create an instance of popup content found in popup.py and popups.kv
        popup_content = PopupContent(self._createPopupErrorLabels(), current_screen)
        self.logDebug(
            'KvOps',
            f'Created a PopupContent instance with popup error labels for screen {self.sm.current}'
        )

        # Create the popup, assign the title, content, etc
        # auto_dismiss prevents clicking outside of the popup to close the popup
        self.pop = Popup(title='',
                         separator_height=0,
                         content=popup_content,
                         size_hint=self.kv_settings['popup size_hint'],
                         auto_dismiss=self.kv_settings['popup auto_dismiss'],
                         )
        log = 'Assigned self.pop as Popup('
        log += f'\n\t\t\ttitle = {self.pop.title},'
        log += f'\n\t\t\tcontent = {popup_content},'
        log += f'''\n\t\t\tsize_hint = {self.kv_settings['popup size_hint']},'''
        log += f'''\n\t\t\tauto_dismiss = {self.kv_settings['popup auto_dismiss']}'''
        log += f'\n\t\t\t)'
        self.logDebug('KvOps', log)

        # Assign the popup
        self.logDebug('KvOps', 'Assigning parent method to popup_content')
        popup_content.assignParentMethod(self.pop.dismiss)

        # ####
        # def update_rectangle(instance, value):
        #     instance.rectangle.pos = instance.pos
        #     instance.rectangle.size = instance.size

        # with self.pop.canvas.before:
        #     Color(1, 1, 1, 1)
        #     self.pop.rectangle = Rectangle(size=popup_content.size, pos=popup_content.pos)
        #     self.pop.bind(pos=update_rectangle, size=update_rectangle)
        # ####

        # Open the popup
        self.logDebug('KvOps', 'Opening the popup..')
        self.pop.open()

        # Make sure the file isn't loaded more than once
        Builder.unload_file(self.kv_settings['kv popup file'])
        self.logDebug('KvLogic', f'Used kivy.lang.Builder.unload_file({self.kv_settings["kv popup file"]})')

    def _createPopupErrorLabels(self):
        '''Create the widgets to give to PopupContent().  This allows PopupContent to add
           child widgets to itself.'''

        log = 'Creating popup error label widgets for a popup with errors:'
        log += f'\n\t\t\t{pprint.pformat(self.popup_errors, indent=4)}'
        self.logDebug('KvLogic', log)

        # List to keep the widgets
        error_labels = []

        # If self.popup_errors is a populated list..
        if isinstance(self.popup_errors, list) and len(self.popup_errors) > 0:

            # Go through the errors and create Label widgets with the messages as the Labels' text
            for error in self.popup_errors:
                error_labels.append(
                    Label(
                        text=error,
                        font_size=24,
                        pos_hint={'x': 0}
                    )
                )

            self.logDebug(
                'KvOps',
                f'Added Labels to error_labels:\n{pprint.pformat(error_labels, indent=4)}'
            )

            self._clearPopupErrors()
            self.logDebug('KvLogic', 'self.popup_errors reset to [] and error_labels returned')
            return error_labels

        else:
            # self.popup_errors is either too short or not a list
            log = 'ERROR: self.popup_errors is either too short or not a list:'
            log += f'\n\t\t\tlength: {len(self.popup_errors)}'
            log += f'\n\t\t\ttype: {type(self.popup_errors)}'
            self.logWarning('KvLogic', log)
            self.logWarning('KvLogic', self.popup_errors)
            self._clearPopupErrors()
            return None

    def buttonPress(self, call=None, screen=None, direction=None):
        '''Do various things like log the user in and change the current screen.
            screen -> string
            command -> function name as string
            direction -> 'left', 'right', 'up', or 'down'

           commands:
                authenticate
                change screen

            implement calling a method by it's name to reduce the size and complexity of this method:
        https://stackoverflow.com/questions/3061/calling-a-function-of-a-module-by-using-its-name-a-string
        https://stackoverflow.com/questions/1855558/call-method-from-string

                '''

        log = 'Button pressed. Received input:'
        log += f'\n\tscreen: {screen}'
        log += f'\n\tcall: {call}'
        log += f'\n\tdirection: {direction}'
        self.logDebug('KvFeedback', log)

        # If call is among the allowed calls or, in other words, if the string matches a method name
        if call in self.validations['allowed button calls']:

            # Access the class method by string name using getattr
            # self is passed to getattr so it knows in what object to search for call
            # Pass the necessary arguments to the method
            getattr(self, call)(screen, direction)

        else:
            log = f"Call {call} is not in self.validations['allowed button calls']"
            self.logCritical('KvFeedback', log)

    def changeScreen(self, screen, direction):
        '''Change to a screen using direction.  Make sure the screen does not need authentication.
        Implement method to check whether the user is logged in.
        '''

        # Check if the user is logged in
        if self.isLoggedIn() is False:
            # If an attempt to change screens to a screen that needs login information is made
            if self.validations['authentication needed'][screen] is True:
                self.logWarning('KvLogic', f'Received a call to change to {screen} without authentication')

            # If someone tries to switch to a valid screen that doesn't need authentication
            elif self.validations['authentication needed'][screen] is False:
                self.sm.current_screen.resetTextInputs()
                self.sm.transition.direction = direction
                self.sm.current = screen
                self.logInfo('KvOps', f'Changed to {screen} going in direction {direction}')

            # If self.validations['authentication needed'][screen] value is not a boolean
            else:
                log = f"self.validations['authentication needed'][screen] should be boolean. Got "
                log += f'{self.authentication_needed[screen]}'
                self.logWarning('App', log)

        # The user is logged in, so let them do what they want
        elif self.isLoggedIn() is True:
            self.sm.transition.direction = direction
            self.sm.current = screen
            self.logInfo('KvOps', f'Changed to {screen} going in direction {direction}')

        else:
            raise Exception('self.isLoggedIn did not return a boolean')

    def login(self, new_screen, direction):
        '''Handles the graphics operations of logging in and calls the self.authenticate method'''

        old_screen = self.sm.current_screen

        # Check formatting of user input
        check = old_screen.checkUserInputFormat()

        # See if check is not False and is also a tuple
        if check is not False and isinstance(check, tuple):

            # Unpack the tuple as individual arguments to self.authenticate
            is_logged_in = self.authenticate(*check)

            # If user successfully logged in
            if is_logged_in:
                # Change the transition properties and current screen
                self.sm.transition.direction = direction
                self.sm.current = new_screen
            # Username or pass is invalid.  Create a popup
            else:
                self.logDebug('DB Ops', 'Login rejected, creating error popup')
                self.popup_errors.append('Invalid username or password')
                self.createPopup()
        else:
            self.createPopup()

        old_screen.resetTextInputs()

    def createAccount(self, new_screen, direction):

        old_screen = self.sm.current_screen

        # Check user input format
        check = old_screen.checkUserInputFormat()
        old_screen.resetTextInputs()

        # If there were no errors
        if len(self.popup_errors) == 0:

            self.logInfo('KvFeedback', f'No errors were found for user input on new_screen {new_screen}')

            # If the formatting is correct
            if check is not False and isinstance(check, tuple):

                # Try to create an account
                self.logDebug('KvOps', 'Requesting account creation..')
                is_logged_in = self.createUser(*check)

                # If the user was successfully created and logged in
                if is_logged_in is True:

                    self.logInfo('KvOps', 'User was successfully logged in! Changing screen')
                    # Change the screen
                    self.sm.transition.direction = direction
                    self.sm.current = new_screen

                # If the account creation failed
                else:
                    self.logError('DB Ops', 'Account creation failed! Creating popup')
                    self.popup_errors.append('Account creation failed for an unknown reason!')

            else:
                self.logError('KvFeedback', 'Formatting errors were not caught by createAccount method')

        else:
            # Errors existed, make a popup
            self.createPopup()

        old_screen.resetTextInputs()
