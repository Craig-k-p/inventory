from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.widget import WidgetException

from resources.utilities import LogMethods
from resources.inventoryobjects import InventoryObject


class Toolbar(BoxLayout, LogMethods):

    app = ObjectProperty(None)
    create_thing_button = ObjectProperty(None)
    create_container_button = ObjectProperty(None)
    toolbar_right = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Toolbar, self).__init__(**kwargs)

        self.__initLog__(file_str=__file__, class_str='Toolbar')

        self.options = [
                Button(
                text='delete',
                size=('40px', '30px'),
                size_hint=(None, None)
            ),
            Button(
                text='edit',
                size=('40px', '30px'),
                size_hint=(None, None)
            ),
            Button(
                text='move',
                size=('40px', '30px'),
                size_hint=(None, None)
            )
        ]

    def checkForScreen(self, screen_str):
        '''Make sure the screen_str is correct before we open a popup. Use app to reference the main
           application instance to check which screen we are using'''
        self.logDebug('Checking app.sm.current for a match')
        self.logDebug(f'self.app.sm.current = {self.app.sm.current}')
        if self.app.sm.current == 'container':
            self.app.buttonPress('createThingPopup', None, None)
        elif self.app.sm.current == 'account':
            self.app.buttonPress('createContainerPopup', None, None)

    def presentOptions(self):
        '''Display toolbar options for selected objects in user's inventory'''
        # If an object is selected, add the widgets to the toolbar
        if self.app.Selection.get().getObj() != None:
            for widget in self.options:
                if widget not in self.toolbar_right.children:
                    self.toolbar_right.add_widget(widget)
            self.options_drawn = True
            # except WidgetException as e:
            #     self.logDebug(f'EXCEPTION: {e}')

        # If an object isn't selected, remove the widgets from the toolbar
        else:
            for widget in self.options:
                if widget in self.toolbar_right.children:
                    self.toolbar_right.remove_widget(widget)
            self.options_drawn = False
                # except WidgetException as e:
                #     self.logDebug(f'EXCEPTION: {e}')
