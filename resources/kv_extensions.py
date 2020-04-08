import pprint
from json import dumps
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
# from kivy.graphics.context_instructions import Color
# from kivy.graphics.vertex_instructions import Rectangle

from resources.inventoryobjects import InventoryObject
from graphics.py.account.rows_container import ContainerDataRow
from graphics.py.account.rows_thing import ThingDataRow
from graphics.py.pre_auth.popups import PopupErrorContent, PopupCreateThingContent, PopupCreateContainerContent
from graphics.py.account.screens import AccountOverviewScreen, ContainerOverviewScreen, ThingOverviewScreen


class KivyExtensions():
    '''Used to separate the Kivy graphics methods needed in MyInventoryApp
       from the MongoEngine database methods needed for the back end.'''

    def buttonPress(self,
                    call=None,
                    screen=None,
                    direction=None,
                    kv_object_reference=None,
                    object_class_str=None,
                    close_popup_on_success=True
                    ):
        ''' Do various things like log the user in and change the current screen.
            screen -> string
            command -> function name as string
            direction -> 'left', 'right', 'up', or 'down'
            kv_object_reference -> kv popup content instance (defined in popups.kv)
            object_class_str -> 'Thing' or 'Container'

            Commands:
                'changeScreen',
                'createAccount',
                'login',
                'createThingPopup',
                'createContainerPopup',
                'createInventoryObject'

            Resources:
        https://stackoverflow.com/questions/3061/calling-a-function-of-a-module-by-using-its-name-a-string
        https://stackoverflow.com/questions/1855558/call-method-from-string

                '''

        log = 'Button pressed. Received input:'
        log += f'\n\tscreen: {screen}'
        log += f'\n\tcall: {call}'
        log += f'\n\tdirection: {direction}'
        self.logDebug(log)

        # If call is among the allowed calls or, in other words, if the string matches a
        # method name
        if call in self.validations['allowed button calls']:

            # Access the class method by string name using getattr
            # self is passed to getattr so it knows in what object to search for call
            method = getattr(self, call)

            if kv_object_reference is None:
                # Pass the necessary arguments to the method
                verdict = method(screen, direction)
            else:
                verdict = method(object_class_str, kv_object_reference)

            if close_popup_on_success is True:
                if verdict is True:
                    self.pop.dismiss()

        else:
            log = f"Call {call} is not in self.validations['allowed button calls']"
            self.logCritical(log)

    def changeScreen(self, screen, direction):
        '''Change to a screen using direction.  Make sure the screen does not need
        authentication.
        Implement method to check whether the user is logged in.
        '''
        try:
            self.sm.current_screen.resetTextInputs()
        except AttributeError:
            pass
        self.sm.transition.direction = direction
        self.sm.current = screen
        self.logInfo(f'Changed to {screen} going in direction {direction}')

        try:
            # Update visible inventory widgets
            InventoryObject.updateWidgets(self.sm.current_screen.data_grid)
        except AttributeError:
            pass

    def createAccount(self, new_screen, direction):
        pass

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

        # Load the popup content from file and create an instance of PopupContent
        Builder.load_file(self.kv_settings['kv popup file'])
        self.logDebug(f'kivy.lang.Builder loaded the file\
         {self.kv_settings["kv popup file"]}')

        # Create an instance of popup content found in popup.py and popups.kv
        popup_content = PopupErrorContent(self._createPopupErrorLabels(), current_screen)
        self.logDebug(
            f'Created a PopupErrorContent instance with popup error labels for screen\
             {self.sm.current}'
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
        self.logDebug(log)

        # Assign the popup
        self.logDebug('Assigning parent method to popup_content')
        popup_content.assignParentMethod(self.pop.dismiss)

        # Open the popup
        self.logDebug('Opening the popup..')
        self.pop.open()

        # Make sure the file isn't loaded more than once
        Builder.unload_file(self.kv_settings['kv popup file'])
        self.logDebug(
            f'Used kivy.lang.Builder.unload_file({self.kv_settings["kv popup file"]})'
        )

    def createContainerPopup(self, screen=None, direction=None):
        # Load the popup content from file and create an instance of PopupContent
        self.logDebug(
            f'kivy.lang.Builder is loading {self.kv_settings["kv popup file"]}'
        )
        Builder.load_file(self.kv_settings['kv popup file'])

        # Create an instance of PopupCreateThingContent found in popup.py and popups.kv
        popup_content = PopupCreateContainerContent()
        self.logDebug(
            f'Created a PopupCreateContainerContent instance for screen "{self.sm.current}"'
        )

        # Create the popup, assign the title, content, etc
        # auto_dismiss prevents clicking outside of the popup to close the popup
        self.pop = Popup(title='Create a new container',
                         title_size=24,
                         separator_height=2,
                         content=popup_content,
                         size_hint=(.9, .9),
                         auto_dismiss=self.kv_settings['popup auto_dismiss'],
                         )
        log = 'Assigned self.pop as Popup('
        log += f'\n\t\t\ttitle = {self.pop.title},'
        log += f'\n\t\t\tcontent = {popup_content},'
        log += f'''\n\t\t\tsize_hint = {self.kv_settings['popup size_hint']},'''
        log += f'''\n\t\t\tauto_dismiss = {self.kv_settings['popup auto_dismiss']}'''
        log += f'\n\t\t\t)'
        self.logDebug(log)

        # # Assign the popup
        # self.logDebug('Kv Ops', 'Assigning parent method to popup_content')
        # popup_content.assignParentMethod(self.pop.dismiss)

        # Open the popup
        self.logDebug('Opening the popup..')
        self.pop.open()

        # Make sure the file isn't loaded more than once
        Builder.unload_file(self.kv_settings['kv popup file'])
        self.logDebug(
            f'Used kivy.lang.Builder.unload_file({self.kv_settings["kv popup file"]})'
        )

    def createThingPopup(self, screen=None, direction=None):
        # Load the popup content from file and create an instance of PopupContent
        self.logDebug(f'kivy.lang.Builder is loading {self.kv_settings["kv popup file"]}')
        Builder.load_file(self.kv_settings['kv popup file'])

        # Create an instance of PopupCreateThingContent found in popup.py and popups.kv
        popup_content = PopupCreateThingContent()
        self.logDebug(
            f'Created a PopupCreateThingContent instance for screen "{self.sm.current}"'
        )

        # Create the popup, assign the title, content, etc
        # auto_dismiss prevents clicking outside of the popup to close the popup
        self.pop = Popup(title='Create a new object',
                         title_size=24,
                         separator_height=2,
                         content=popup_content,
                         size_hint=(.9, .9),
                         auto_dismiss=self.kv_settings['popup auto_dismiss'],
                         )
        log = 'Assigned self.pop as Popup('
        log += f'\n\t\t\ttitle = {self.pop.title},'
        log += f'\n\t\t\tcontent = {popup_content},'
        log += f'''\n\t\t\tsize_hint = {self.kv_settings['popup size_hint']},'''
        log += f'''\n\t\t\tauto_dismiss = {self.kv_settings['popup auto_dismiss']}'''
        log += f'\n\t\t\t)'
        self.logDebug(log)

        # # Assign the popup
        # self.logDebug('Kv Ops', 'Assigning parent method to popup_content')
        # popup_content.assignParentMethod(self.pop.dismiss)

        # Open the popup
        self.logDebug('Opening the popup..')
        self.pop.open()

        # Make sure the file isn't loaded more than once
        Builder.unload_file(self.kv_settings['kv popup file'])
        self.logDebug(
            f'Used kivy.lang.Builder.unload_file({self.kv_settings["kv popup file"]})'
        )

    def createUserScreens(self):
        '''Create user screens after the user has been logged in to be sure the widgets are
        able to get the information they need!'''
        self.sm.add_widget(AccountOverviewScreen())
        self.sm.add_widget(ContainerOverviewScreen())
        self.sm.add_widget(ThingOverviewScreen())

    def login(self, new_screen, direction):
        '''Handles the graphics operations of logging in and calls the self.authenticate
        method'''

        old_screen = self.sm.current_screen
        # Create the screens
        self.createUserScreens()

        # Change the transition properties and current screen
        self.sm.transition.direction = direction
        self.sm.current = new_screen

        old_screen.resetTextInputs()

    def _clearPopupErrors(self):
        self.popup_errors = []

    def _createPopupErrorLabels(self):
        '''Create the widgets to give to PopupContent().  This allows PopupContent to add
           child widgets to itself.'''

        log = 'Creating popup error label widgets for a popup with errors:'
        log += f'\n\t\t\t{pprint.pformat(self.popup_errors, indent=4)}'
        self.logDebug(log)

        # List to keep the widgets
        error_labels = []

        # If self.popup_errors is a populated list..
        if isinstance(self.popup_errors, list) and len(self.popup_errors) > 0:

            # Go through the errors and create Label widgets with the messages as the Labels'
            # text
            for error in self.popup_errors:
                error_labels.append(
                    Label(
                        text=error,
                        font_size=24,
                        pos_hint={'x': 0}
                    )
                )

            self.logDebug(
                f'Added Labels to error_labels:\n{pprint.pformat(error_labels, indent=4)}'
            )

            self._clearPopupErrors()
            self.logDebug('self.popup_errors reset to [] and error_labels returned')
            return error_labels

        else:
            # self.popup_errors is either too short or not a list
            log = 'ERROR: self.popup_errors is either too short or not a list:'
            log += f'\n\t\t\tlength: {len(self.popup_errors)}'
            log += f'\n\t\t\ttype: {type(self.popup_errors)}'
            self.logWarning(log)
            self.logWarning(self.popup_errors)
            self._clearPopupErrors()
            return None

    def _isValidPopupUserInput(self, popup_content):
        '''Verify that user input from the popup is valid'''
        required = self.kv_settings['popup required fields']
        self.logDebug(f'Required input keys: {required}')

        # Loop through the popup_content.ids (text_inputs) keys and check if they're required
        # Add the key of required TextInputs with empty text fields to the error_keys list
        error_keys = []
        for key in popup_content.ids:
            if key in required and popup_content.ids[key].text == '':
                self.logDebug(f'Found error for key: {key}')
                error_keys.append(key)

        if len(error_keys) > 0:
            popup_content.updateTextInputErrors(error_keys)
            return False

        # Return True if no empty fields were found
        return True


    def _getObjectCreationUserInput(self, popup_content):
        '''Get user input text from popup fields for container and object creation
           Takes popup_content instance as an argument to access the TextInput instances
           Returns kwargs without empty values
           kwargs keys must match MongoEngine.Documents' Thing or Container attributes
             since it is being passed directly for instantiation'''

        # Key-word argument dictionary
        data = {}
        # For each key in popup_content instance ids dictionary
        # Holds child widgets with their defined id as a key
        for key in popup_content.ids:
            # Check that the child widget is a TextInput to avoid AttributeErrors
            if isinstance(popup_content.ids[key], TextInput):
                data[key] = popup_content.ids[key].text

        self.logDebug(f'data: {data}')

        return data
