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

    def checkForScreen(self, screen_str, app):
        '''Make sure the screen_str is correct before we open a popup. Use app to reference the main
           application instance to check which screen we are using'''
        self.logDebug('Checking app.sm.current for a match')
        self.logDebug(f'app.sm.current = {app.sm.current}')
        if app.sm.current == 'container':
            app.buttonPress('createThingPopup', None, None)
        elif app.sm.current == 'account':
            app.buttonPress('createContainerPopup', None, None)

    def logObjects(self, app):
        '''Call self.getObjects and put them into the log'''
        self.logInfo(f'Toolbar.logObjects called')

        objects = app.getObjects()
