from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.widget import WidgetException

from resources.utilities import LogMethods
from resources.inventoryobjects import Container


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

    def checkForScreen(self, create_inventory=False, get_stats=False):
        '''Use app to reference the main application instance to check which screen we are using'''
        self.logDebug(f'Current screen found to be: {self.app.sm.current}')

        if create_inventory == True:
            self.logDebug(f'Opening the appropriate create item popup')
            if self.app.sm.current == 'contents':
                self.app.thingPopup()
            elif self.app.sm.current == 'containers':
                self.app.containerPopup()

        elif get_stats == True:
            self.logDebug(f'Opening a stats popup')
            self.app.createPopup(stats=True)

        else:
            log = f'Toolbar.checkForScreen does not know what to do without one of create_inventory'
            log += f' or get_stats flags set to True'
            self.logError()

    def editObject(self):
        '''Open a popup to edit the selected object'''
        if self.app.sm.current == 'contents':
            self.app.thingPopup(thing=self.app.selection.get(suppress=True).getObj())
        elif self.app.sm.current == 'containers':
            self.app.containerPopup(container=self.app.selection.get(suppress=True).getObj())

    def mergeObject(self):
        '''Merge the contents of this container with another'''
        self.app.createPopup(merge=True)

    def moveObject(self):
        '''Open a popup to give the user options for moving the inventory to a new container'''
        self.app.createPopup(move=True)

    def presentOptions(self):
        '''Display toolbar options for selected objects in user's inventory'''

        if self.options == None:
            # Allows us to assign call_delete to the on_press variable without calling
            # the function within the lambda declaration
            self.call_delete = lambda call_return : self.app.sm.current_screen.data_grid.deleteObject()

            # Allows us to assign call_edit to the on_press variable without calling
            # the function within the lambda declaration
            self.call_edit = lambda call_return : self.editObject()

            # Allows us to assign call_move to the on_press variable without calling
            # the function within the lambda declaration
            self.call_move = lambda call_return : self.moveObject()

            # Allows us to assign call_merge to the on_press variable without calling
            # the function within the lambda declaration
            self.call_merge = lambda call_return : self.mergeObject()

            self.options = [
                    Button(
                        text='Delete',
                        size=('65px', '30px'),
                        size_hint=(None, None),
                        on_release=self.call_delete,
                        pos_hint={'center_x': .25, 'center_y': .5}
                    ),
                    Button(
                        text='Edit',
                        size=('50px', '30px'),
                        size_hint=(None, None),
                        on_release=self.call_edit,
                        pos_hint={'center_x': .25, 'center_y': .5}
                    ),
                    Button(
                        text='Move',
                        size=('55px', '30px'),
                        size_hint=(None, None),
                        on_release=self.call_move,
                        pos_hint={'center_x': .25, 'center_y': .5}
                    ),
            ]

            self.option_merge = Button(
                        text='Merge',
                        size=('64px', '30px'),
                        size_hint=(None, None),
                        on_release=self.call_merge,
                        pos_hint={'center_x': .25, 'center_y': .5}
                        )

        selection = self.app.selection.get(suppress=True).getObj()

        # If an object is selected, add the widgets to the toolbar
        if selection != None:
            # For each widget in self.options list
            for widget in self.options:
                # If it is not in the toolbar
                if widget not in self.toolbar_right.children:
                    # Add the widget to the toolbar
                    self.toolbar_right.add_widget(widget, index=-1)
            # Add a special option for containers
            if self.option_merge not in self.toolbar_right.children:
                if isinstance(selection, Container):
                    self.toolbar_right.add_widget(self.option_merge, index=-1)

            self.options_drawn = True

        # If an object isn't selected
        else:
            # For each widget in self.options list
            for widget in self.options:
                # If the widget is on the toolbar
                if widget in self.toolbar_right.children:
                    # Remove the widget from the toolbar
                    self.toolbar_right.remove_widget(widget)

            # Remove the merge button
            if self.option_merge in self.toolbar_right.children:
                self.toolbar_right.remove_widget(self.option_merge)

            self.options_drawn = False
