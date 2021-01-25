from json import dumps
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from resources.inventory import Inventory
from graphics.row2 import ContainerDataRow, ThingDataRow
from graphics.popups2 import PopupContentThing, PopupContentContainer, PopupContentStats
from graphics.popups2 import PopupContentError, PopupContentList, PopupContentWarningDelete
from graphics.popups2 import PopupContentCreatePassword, PopupContentPassword
from graphics.screens2 import AccountOverviewScreen, ContainerOverviewScreen


class KivyExtensions():
    '''Used to separate the Kivy graphics methods needed in MyInventoryApp
       from the methods handling the data'''

    def closePopup(self, popup_content):
        if popup_content.inventory_object == None:
            self.createInventory(popup_content)
        else:
            self.updateObjectData(popup_content)

        self.pop.dismiss()

    def changeScreen(self, screen):
        '''Change to a screen using direction'''
        if isinstance(screen, int):
            screen = str(screen)
            self.logDebug('Changed screen from int to str')

        if screen == 'back':
            Inventory.search_term = ''
            if self.sm.current_screen.name == 'inventory':
                self.sm.current = 'load file'
                self.restart()
            elif self.sm.current_screen.name == 'contents':
                self.sm.current = screen
                #  Update the selected object to match the current screen
                self.selection(self.selection.getLast().getObj())
                # Update visible inventory
                Inventory.updateWidgets(self.sm.current_screen.data_grid)
        else:
            try:
                self.sm.current_screen.resetTextInputs()
            except AttributeError:
                pass
            self.sm.current = screen
            try:
                # Update visible inventory widgets
                Inventory.updateWidgets(self.sm.current_screen.data_grid)
            except AttributeError:
                pass

    def createPopup(self, warn=False, merge=False, move=False, stats=False, errors=None,
                    create_password=False, prompt_password=False, file=None):
        '''Method that does the following:
            -Load the kv file that defines what goes into the popup
            -Create an instance of Popup
            -Draw the popup to the screen
            -Unload the file to avoid errors'''

        # Load the popup content from file and create an instance of PopupContent
        Builder.load_file(self.settings['kv popup file'])

        popup_size_hint = self.settings['popup size_hint']
        popup_size = self.settings['popup size']

        try:
            selected = self.selection.get(suppress=True).getObj()
        except AttributeError:
            pass

        if move == True:
            pop_title = f'Move {selected.description}'
            pop_title += f' from {Inventory.getByID(selected.container).description} to..'
            popup_content = PopupContentList(self)

        elif merge == True:
            pop_title = f'Merge contents of {selected.description} into..'
            popup_content = PopupContentList(self)

        elif warn == True:
            pop_title = f'Delete {selected.description}'
            popup_content = PopupContentWarningDelete()
            popup_size = (500,300)

        elif stats == True:
            pop_title = 'Inventory Stats'
            popup_content = PopupContentStats()
            popup_size = (500, 600)

        elif create_password == True:
            pop_title = 'Create a new password'
            popup_content = PopupContentCreatePassword(self)
            popup_size = (500, 450)

        elif prompt_password == True:
            pop_title = 'Enter your password'
            popup_content = PopupContentPassword(self, file)
            popup_size = (500, 250)

        elif isinstance(errors, list):
            pop_title = 'Error'
            popup_content = PopupContentError(errors)
            popup_size = (500, 285 + (60 * len(errors)))

        else:
            self.logWarning('move, merge, and warn flags are all False. Returning.')
            # Make sure the file isn't loaded more than once
            Builder.unload_file(self.settings['kv popup file'])
            return

        # Create the popup, assign the title, content, etc
        # auto_dismiss prevents clicking outside of the popup to close the popup
        self.pop = Popup(title=pop_title,
                         title_size=24,
                         separator_height=2,
                         content=popup_content,
                         size_hint=popup_size_hint,
                         size=popup_size,
                         auto_dismiss=self.settings['popup auto_dismiss'],
                         )

        # Open the popup
        self.logDebug('Opening the popup..')
        self.pop.open()

        if move == True or errors != None:
            popup_content.fill()
        elif merge == True:
            popup_content.fill(merge=True)

        # Make sure the file isn't loaded more than once
        Builder.unload_file(self.settings['kv popup file'])

    def createUserScreens(self):
        '''Create user screens after the user has been logged in to be sure the widgets are
        able to get the information they need!'''
        self.sm.add_widget(InventoryOverviewScreen(self))
        self.sm.current = 'inventory'

    def containerPopup(self, screen=None, direction=None, container=None):
        # Load the popup content from file and create an instance of PopupContent
        Builder.load_file(self.settings['kv popup file'])

        # Create an instance of PopupContainerContent found in popup.py and popups.kv
        popup_content = PopupContentContainer(container)
        # If a container instance was provided, this is an edit
        if container != None:
            pop_title = f'Edit {self.selection.get(suppress=True).getObj().description}'
        # If not, this is a new container
        else:
            pop_title = 'Add container to inventory'

        # Create the popup, assign the title, content, etc
        # auto_dismiss prevents clicking outside of the popup to close the popup
        self.pop = Popup(title=pop_title,
                         title_size=24,
                         separator_height=2,
                         content=popup_content,
                         size_hint=(.9, .9),
                         auto_dismiss=self.settings['popup auto_dismiss'],
                         )
        # If a container was provided to edit..
        if container != None:
            # Set the text input fields to match the saved values
            popup_content.setInventoryValues()

        # Open the popup
        self.logDebug('Opening the popup..')
        self.pop.open()

        # Make sure the file isn't loaded more than once
        Builder.unload_file(self.settings['kv popup file'])

    def _clearPopupErrors(self):
        self.popup_errors = []

    def _createPopupErrorLabels(self):
        '''Create the widgets to give to PopupContent().  This allows PopupContent to add
           child widgets to itself.'''

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

            self._clearPopupErrors()
            return error_labels

        else:
            self.logWarning(self.popup_errors)
            self._clearPopupErrors()
            return None

    def _getObjectCreationUserInput(self, popup_content):
        '''Get user input text from popup fields for inventory creation
           Takes popup_content instance as an argument to access the TextInput instances
           Returns kwargs without empty values'''

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
