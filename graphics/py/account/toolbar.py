from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.widget import WidgetException

from resources.utilities import LogMethods
# from resources.inventoryobjects import InventoryObject


class Toolbar(BoxLayout, LogMethods):

    app = ObjectProperty(None)
    search = ObjectProperty(None)
    create_thing_button = ObjectProperty(None)
    create_container_button = ObjectProperty(None)
    toolbar_right = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Toolbar, self).__init__(**kwargs)

        self.__initLog__(file_str=__file__, class_str='Toolbar')

        self.options = None

    def checkForScreen(self):
        '''Use app to reference the main application instance to check which screen we are using'''
        self.logDebug('Checking app.sm.current for a match')
        self.logDebug(f'self.app.sm.current = {self.app.sm.current}')
        if self.app.sm.current == 'container':
            self.app.buttonPress('createThingPopup', None, None)
        elif self.app.sm.current == 'account':
            self.app.buttonPress('createContainerPopup', None, None)

    def editObject(self):
        '''Open a popup to edit the selected object'''
        if self.app.sm.current == 'container':
            self.app.buttonPress('createThingPopup', None, None)
        elif self.app.sm.current == 'account':
            self.app.buttonPress('createContainerPopup', None, None)

    def presentOptions(self):
        '''Display toolbar options for selected objects in user's inventory'''

        if self.options == None:
            # Allows us to assign call_delete to the on_press variable without calling
            # the function within the lambda declaration
            call_delete = lambda call_return : self.app.sm.current_screen.data_grid.deleteObject()

            # Allows us to assign call_edit to the on_press variable without calling
            # the function within the lambda declaration
            call_edit = lambda call_return : print()

            # Allows us to assign call_move to the on_press variable without calling
            # the function within the lambda declaration
            call_move = lambda call_return : print()

            self.options = [
                    Button(
                        text='delete',
                        size=('50px', '30px'),
                        size_hint=(None, None),
                        on_release=call_delete,
                        pos_hint={'center_x': .25, 'center_y': .5}
                    ),
                    Button(
                        text='edit',
                        size=('38px', '30px'),
                        size_hint=(None, None),
                        on_release=call_edit,
                        pos_hint={'center_x': .25, 'center_y': .5}
                    ),
                    Button(
                        text='move',
                        size=('47px', '30px'),
                        size_hint=(None, None),
                        on_release=call_move,
                        pos_hint={'center_x': .25, 'center_y': .5}
                    ),
            ]

        # If an object is selected, add the widgets to the toolbar
        if self.app.Selection.get(suppress=True).getObj() != None:
            # For each widget in self.options list
            for widget in self.options:
                # If it is not in the toolbar
                if widget not in self.toolbar_right.children:
                    # Add the widget to the toolbar
                    self.toolbar_right.add_widget(widget, index=-1)
            self.options_drawn = True

        # If an object isn't selected, remove the widgets from the toolbar
        else:
            # For each widget in self.options list
            for widget in self.options:
                # If the widget is on the toolbar
                if widget in self.toolbar_right.children:
                    # Remove the widget from the toolbar
                    self.toolbar_right.remove_widget(widget)
            self.options_drawn = False
