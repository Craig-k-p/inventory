from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.widget import WidgetException

from resources.utilities import LogMethods
from resources.inventoryobjects import InventoryObject


class Toolbar(BoxLayout, LogMethods):

    create_thing_button = ObjectProperty(None)
    create_container_button = ObjectProperty(None)
    toolbar_right = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Toolbar, self).__init__(**kwargs)

        self.__initLog__(
            file_str=__file__,
            class_str='Toolbar'
        )
        self.app = None

        self.options = {
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
        }

    def checkForScreen(self, screen_str, app):
        '''Make sure the screen_str is correct before we open a popup. Use app to reference the main
           application instance to check which screen we are using'''
        if not self.app:
            self.app = app
        self.logDebug('Checking app.sm.current for a match')
        self.logDebug(f'app.sm.current = {app.sm.current}')
        if app.sm.current == 'container':
            app.buttonPress('createThingPopup', None, None)
        elif app.sm.current == 'account':
            app.buttonPress('createContainerPopup', None, None)

    def presentOptions(self, app):
        if not self.app:
            self.app = app

        if InventoryObject.selected != None:
            try:
                for widget in self.options:
                    self.toolbar_right.add_widget(widget)
                self.options_drawn = True
            except WidgetException:
                pass

        else:
            try:
                for widget in self.options:
                    self.toolbar_right.remove_widget(widget)
                self.options_drawn = False
            except WidgetException:
                pass
