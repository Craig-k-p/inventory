import pprint

from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, ListProperty

from resources.utilities import LogMethods


class PopupErrorContent(GridLayout, LogMethods):
    '''A class linked to popups.kv class definition'''

    # Grab the BoxLayout from kv/popups.kv
    box = ObjectProperty(None)

    def __init__(self, widgets, current_screen, is_yes_no=False, **kwargs):
        '''Grab a list of child widgets to be added to the popup after self.parent (reference to the parent
           popup) is assigned.
           widgets -> list of Kivy widgets'''

        # Allows us to call our own PopupContent.__init__() without overriding Kivy's FloatLayout.__init__()
        super(PopupErrorContent, self).__init__(**kwargs)
        self.cols = 1
        self.pos_hint = {'x': 0, 'y': 0}

        # Initialize the log for this class instance
        self.__initLog__(
            file_str='kv_popup',
            class_str='PopupContent'
        )

        # Assign widgets, current_screen, and is_yes_no variables to class variables
        self.widgets = widgets
        self.current_screen = current_screen
        self.is_yes_no = is_yes_no
        log = 'New instance:\n\t\tPopupContent('
        log += f'\n\t\t\twidgets = {self.widgets},'
        log += f'\n\t\t\tcurrent_screen = {self.current_screen.manager.current},'
        log += f'\n\t\t\tis_yes_no = {self.is_yes_no}'
        self.logDebug('Kv Ops', log)

    def assignParentMethod(self, parentMethod):
        '''Allows us to reference the popup from the kv file as root.parent.do_something.
           See kv_extensions.py > KivyExtensions.createPopup() for usage.
           parentMethod -> method to be executed by popup button'''

        # Method to be executed by the popup button
        self.parentMethod = parentMethod
        self.logDebug('Kv Logic', f'Recieved parentMethod: {parentMethod.__name__}')

        # Add the child widgets to the popup
        self._assignChildren()

    def _assignChildren(self):
        '''Loop through self.labels list of child widgets and add them to the popup'''

        # If we have a populated list of widgets
        if isinstance(self.widgets, list) and len(self.widgets) > 0:

            # Add each widget to the parent before it is drawn
            for widget in self.widgets:
                self.box.add_widget(widget)

            self.logInfo('Kv Ops', f'Added widgets to popup:\n{pprint.pformat(self.widgets)}')

            if self.is_yes_no is False:
                # Create a button
                btn = Button(
                    text=self.current_screen.popup_text['button'],
                    font_size=18,
                    size=(200, 50),
                    size_hint=(.5, 0),
                    id='button',
                    pos_hint={'center_x': .5}
                )
                btn.bind(on_release=self.parentMethod)
                self.logDebug('Kv Ops', 'self.is_yes_no is False.  Added a single button to popup')
                # Add a button to the BoxLayout with the given text and parentMethod
                self.box.add_widget(btn)

            else:
                print('Not implemented --- kv_popup.PopupContent._assignChildren')
                log = 'self.is_yes_no is True.  Added a yes/no button pair'
                self.logError('Kv Ops', 'Not implemented!  self.is_yes_no is True')

        else:
            log = f'Error!  self.widgets is either not a list or is empty:'
            log += f'\n\t\t\ttype: {type(self.widgets)}'
            log += f'\n\t\t\tcontent: {self.widgets}'
            self.logWarning('Kv Ops', log)


class PopupCreateThingContent(ScrollView, LogMethods):
    '''A class linked to popups.kv class definition'''
    description = ObjectProperty(None)
    value = ObjectProperty(None)
    weight = ObjectProperty(None)
    tags = ObjectProperty(None)
    inputs = ListProperty(None)

    def __init__(self, **kwargs):
        super(PopupCreateThingContent, self).__init__(**kwargs)

        # Initialize the log for this class instance
        self.__initLog__(
            file_str='popups',
            class_str='PopupCreateThingContent'
        )

    def updateTextInputErrors(self, keys):
        '''Change the text inputs with an error to a red tone. Accepts a list of keys
           as input'''
        self.logDebug('KV Ops', 'Changing error TextInputs to a red tone.')


class PopupCreateContainerContent(ScrollView, LogMethods):
    '''A class linked to popups.kv class definition'''
    description = ObjectProperty(None)
    value = ObjectProperty(None)
    weight = ObjectProperty(None)
    tags = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PopupCreateContainerContent, self).__init__(**kwargs)
        self.__initLog__(
            file_str='popups',
            class_str='PopupCreateContainerContent'
        )

    def updateTextInputErrors(self, keys):
        '''Change the text inputs with an error to a red tone. Accepts a list of keys
           as input'''
        self.logDebug('KV Ops', f'{keys} TextInput fields being changed to red')

        for key in keys:
            self.ids[key].error = True

    # def _setBackgroundColor(self):
    #     '''Determine what color to set the background'''
    #     if self.focus == True:
    #         self.


class PopInput(TextInput):
    '''An input with special functions'''
    def __init__(self, **kwargs):
        super(PopInput, self).__init__(**kwargs)

    # def _setBackgroundColor(self):
    #     if self.focus == True:
    #         return (.8,.8,1,1)
    #     elif self.error == True:
    #         return (1,.7,.7,1)
    #     else:
    #         return (1,1,1,1)
