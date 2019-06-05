from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from resources.utilities import LogMethods


class Toolbar(BoxLayout, LogMethods):

    create_thing_button = ObjectProperty(None)
    create_container_button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Toolbar, self).__init__(**kwargs)

        self.__initLog__(
            file_str=__file__,
            class_str='Toolbar'
        )

    def checkForScreen(self, screen_str, app, popup_method_str):
        '''Make sure the screen_str is correct before we open a popup. Use app to reference the main
           application instance to check which screen we are using'''
        self.logDebug('Kv Feedback', 'Checking app.sm.current for a match')
        self.logDebug('Kv Feedback', f'app.sm.current = {app.sm.current}')
        if screen_str == app.sm.current:
            self.logDebug('Kv Logic', f'Checked if screen_str was equal to app.sm.current and found True!')
            app.buttonPress(popup_method_str, None, None)
