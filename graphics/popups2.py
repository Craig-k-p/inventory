import pprint

from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, ListProperty

from resources.utilities import LogMethods
from resources.inventory import Inventory


class PopLabel(Label):
    '''Defined in popups.kv'''
class PopButton(Button):
    '''Defined in popups.kv'''
class CenterAnchorLayout(AnchorLayout):
    '''FileButton class declared in screens.kv'''


class MoveButton(Button, LogMethods):
    def __init__(self, **kwargs):
        super(MoveButton, self).__init__(**kwargs)
        self.__initLog__(file_str='popups.py', class_str='MoveButton')

    def move(self):
        '''Move the inventory item to a new container'''
        if isinstance(self.item_to_move, Thing):
            self.destination_container.addThing(self.item_to_move.ID, new_instance=False)
        elif isinstance(self.item_to_move, Container):
            pass
        else:
            self.parent.parent.parent.parent.parent.dismiss()
            self.logWarning(f'Received the wrong type for self.item_to_move: {type(self.item_to_move)}')
            self.logWarning('Was expecting Container or Thing type')

    def merge(self):
        '''Merge the contents of the chosen containers'''
        self.origin_container.merge(self.destination_container.ID)

class PopupContentCreatePassword(GridLayout, LogMethods):
    '''A class linked to it's popups.kv class definition. Handles user
       password input for file saving/loading'''
    prompt = ObjectProperty(None)
    prompt_b = ObjectProperty(None)
    def __init__(self, app, **kwargs):
        super(PopupContentCreatePassword, self).__init__(**kwargs)
        self.__initLog__(file_str='popups', class_str='PopupContentCreatePassword')
        self.app = app

    def checkFormat(self):
        '''Check for input errors to determine if we should accept or reject user input'''
        if len(self.prompt.text) < 8 or self.prompt.text != self.prompt_b.text:
            self.prompt.text_input.error, self.prompt_b.text_input.error = True, True
            self.logDebug('Password error')
        else:
            self.prompt.error, self.prompt_b.error = False, False
            self.app.sec.createPassword()
            self.app.pop.dismiss()
            self.app.is_new_inventory = True
            self.app.user_file_en = True
            self.app.createUserScreens()


class PopupContentError(GridLayout, LogMethods):
    '''A class linked to popups.kv class definition'''
    def __init__(self, errors, **kwargs):
        '''Takes a list of child widgets to be added to the popup after self.parent
           (reference to the parent popup) is assigned.
           widgets -> list of Kivy widgets'''
        super(PopupContentError, self).__init__(**kwargs)
        self.__initLog__(file_str='kv_popup', class_str='PopupContent')
        self.errors = errors
        self.logDebug('Creating popup to notify user of errors')

    def fill(self):
        '''Fill the popup with error labels and an "OK" button'''
        self.logDebug('Filling the popup with error message(s)')

        layout = GridLayout(cols=1)

        for error in self.errors:
            widget = CenterAnchorLayout()
            widget.add_widget(PopLabel(text=error))
            layout.add_widget(widget)

        self.add_widget(layout)

        widget = CenterAnchorLayout()
        widget.add_widget(
            PopButton(
                text='continue',
                size_hint=(None, None),
                size=(120, 70),
                on_release=self.app.pop.dismiss
                )
            )
        layout2 = GridLayout(cols=1, size_hint=(1,1))
        layout2.add_widget(widget)
        self.add_widget(layout2)

class PopupContentPassword(GridLayout, LogMethods):
    '''A class linked to it's popups.kv class definition. Handles user
       password input for file saving/loading'''
    prompt = ObjectProperty(None)
    def __init__(self, app, file, **kwargs):
        super(PopupContentPassword, self).__init__(**kwargs)
        self.__initLog__(file_str='popups', class_str='PopupContentPassword')
        self.app = app
        self.user_file = file

    def checkPassword(self):
        '''See if user password unlocks the file'''
        self.prompt.text_input.error = False
        if self.app.start(self.user_file, encrypted=True) == False:
            self.prompt.text_input.error = True
        else:
            self.prompt.text_input.error = False
            self.app.pop.dismiss()

    def checkFormat(self, popup_content, object_class_str):
        '''Check for input errors to determine if we should accept or reject user input'''
        self.error = 0

        if len(self.description.text) == 0:
            self.description.error = True
            self.error += 1
        else:
            self.description.error = False

        try:
            float(self.usd_value.text)
            self.usd_value.error = False
        except ValueError:
            self.usd_value.error = True
            self.error += 1

        try:
            float(self.weight.text)
            self.weight.error = False
        except ValueError:
            self.weight.error = True
            self.error += 1

        if self.error > 0:
            pass
        else:
            self.app.closePopup(popup_content, object_class_str)


class PopupContentInventory(ScrollView, LogMethods):
    '''A class linked to popups.kv class definition'''
    description = ObjectProperty(None)
    usd_value = ObjectProperty(None)
    weight = ObjectProperty(None)
    tags = ObjectProperty(None)
    app = ObjectProperty(None)
    submit_button = ObjectProperty(None)

    def __init__(self, inventory, **kwargs):
        super(PopupContentInventory, self).__init__(**kwargs)
        self.__initLog__(file_str='popups', class_str='PopupContentInventory')
        self.inventory = inventory

        # If inventory was passed as an argument..
        if self.inventory != None:
            self.submit_button.text = 'Confirm'
        # If inventory wasn't passed as an argument..
        else:
            self.submit_button.text = 'Add to inventory'

        self.logDebug(f'Popup.tags: {type(self.tags)}')

    def setContainerValues(self):
        '''Fill the textinput boxes with the object's data'''
        self.description.text = self.inventory.description
        self.usd_value.text = self.inventory.usd_value
        self.weight.text = self.inventory.weight
        tags_str = self.inventory.tag_search_str.replace(' ', '_')
        tags_str = tags_str.replace('\n', ' ')
        self.tags.text = tags_str

    def updateTextInputErrors(self, keys):
        '''Change the text inputs with an error to a red tone. Accepts a list of keys
           as input'''
        self.logDebug(f'{keys} TextInput fields being changed to red')

        for key in keys:
            self.ids[key].error = True

    def checkFormat(self, popup_content, object_class_str):
        '''Check for input errors to determine if we should accept or reject user input'''
        self.error = 0

        if len(self.description.text) == 0:
            self.description.error = True
            self.error += 1
        else:
            self.description.error = False

        try:
            float(self.usd_value.text)
            self.usd_value.error = False
        except ValueError:
            self.usd_value.error = True
            self.error += 1

        try:
            float(self.weight.text)
            self.weight.error = False
        except ValueError:
            self.weight.error = True
            self.error += 1

        if self.error > 0:
            pass
        else:
            self.app.closePopup(popup_content)


class PopInput(TextInput):
    '''An input with special functions'''


class PopupContentMoveContainer(GridLayout):
    '''Used to add submit and cancel buttons to container move popups'''
    submit_button = ObjectProperty(None)


class PopupContentList(ScrollView, LogMethods):
    '''A popup class for moving inventory between containers'''
    pop_grid = ObjectProperty(None)

    def __init__(self, app, **kwargs):
        super(PopupContentList, self).__init__(**kwargs)
        self.__initLog__('popups.py', 'PopupContentList')
        self.logDebug('Preparing a popup')
        self.app = app

    # def fill(self, merge=False):
    #     '''Fills the popup with buttons for the user'''

    #     # Get the selected item to move and the container that it is getting
    #     # moved from so we don't give that container as an option
    #     item_to_move = self.app.selection.get(suppress=True).getObj()
    #     origin_container = self.app.selection.getLastContainer().getObj()

    #     # If the selected item to be moved is a Thing instance
    #     if isinstance(item_to_move, Thing) or merge == True:

    #         self.logDebug(f'Filling popup for {item_to_move}')

    #         layout = AnchorLayout(anchor_x='center')
    #         layout.add_widget(
    #             Button(
    #                 text='Cancel',
    #                 on_release=self.app.pop.dismiss,
    #                 size_hint=(None, None),
    #                 size=(250, 50),
    #                 color=self.app.settings['text color'],
    #                 font_size='22sp',
    #                 bold=True
    #                 )
    #             )
    #         self.pop_grid.add_widget(layout)

    #         # Get Container instances from the containers dictionary so we
    #         for key in Container.objs:

    #             # If this is not the origin_container, make a button for the container
    #             if Container.objs[key] != origin_container:
    #                 layout = CenterAnchorLayout()

    #                 new_container = Container.objs[key]

    #                 # Create a button with the container's descrition
    #                 count = new_container.hasContents(count=True)

    #                 if count == 0:
    #                     description = f'{new_container.description} [empty]'
    #                 elif count == 1:
    #                     description = description = f'{new_container.description} [{count} item]'
    #                 else:
    #                     description = f'{new_container.description} [{count} items]'

    #                 popup_button = MoveButton(text=description)

    #                 # Link the Container instance to the button
    #                 popup_button.destination_container = InventoryObject.getByID(key)

    #                 if merge == False:
    #                     popup_button.item_to_move = item_to_move
    #                     popup_button.on_release = popup_button.move
    #                 else:
    #                     popup_button.origin_container = origin_container
    #                     popup_button.on_release = popup_button.merge

    #                 layout.add_widget(popup_button)

    #                 # Add the button to the grid widget
    #                 self.pop_grid.add_widget(layout)

        else:
            log = f'The selected object was not an Inventory instance. Got {type(item_to_move)}'
            self.logWarning(log)
            self.app.pop.dismiss()


class PopupContentStats(GridLayout, LogMethods):
    '''Show the user stats for entire inventory'''
class PopupContentWarningDelete(ScrollView, LogMethods):
    '''Used to warn the user if they are deleting a container that has contents'''

