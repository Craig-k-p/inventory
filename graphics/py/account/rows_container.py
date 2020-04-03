import random

from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from resources.utilities import LogMethods


class ContainerHeadingRow(GridLayout, LogMethods):
    container = ObjectProperty(None)
    weight = ObjectProperty(None)
    val = ObjectProperty(None)
    loc = ObjectProperty(None)
    tag = ObjectProperty(None)
    opt = ObjectProperty(None)
    my_text = StringProperty(None)
    weight_col_width = NumericProperty(50)
    val_col_width = NumericProperty(65)

    settings = {
        'heading_color': Color(.1, .1, .1, 0.2)
    }

    def __init__(self, **kwargs):
        super(ContainerHeadingRow, self).__init__(**kwargs)
        self.__initLog__(
            'rows_inventory.py',
            'ContainerHeadingRow'
        )

        self.logDebug('Creating a ContainerHeadingRow instance')

    def setHeadingText(self,
                       container='Container',
                       weight='LBS',
                       usd_value='$$',
                       location='Location',
                       tags='Tags',
                       options='Opts'
                       ):
        '''Set the heading text for each child widget Label'''
        log = f'Setting heading Label text values to {container}, {weight}, {usd_value}, '
        log += f'{location}, {tags}, and {options}'
        self.logDebug(log)
        self.logDebug(f'self.weight.label = {self.weight_label.text}')

        self.obj_label.text = 'HELP'
        self.weight_label.text = weight
        self.val_label.text = self.my_text
        self.loc_label.text = location
        self.tag_button.text = tags
        self.opt_button.text = options

        self.logDebug(f'container.label = {self.obj_label.text}')

        log = f'Values: {self.obj_label.text}, {self.weight_label.text}, {self.val_label.text}'
        self.logDebug(log)


class ContainerDataRow(GridLayout, LogMethods):

    obj_label = ObjectProperty(None)
    weight_label = ObjectProperty(None)
    val_label = ObjectProperty(None)
    loc_label = ObjectProperty(None)
    tag_button = ObjectProperty(None)
    opt_button = ObjectProperty(None)
    weight_col_width = NumericProperty(50)
    val_col_width = NumericProperty(65)

    # settings = {
    #     'row_1_color': Color(.1, .1, .1, 0.2),
    #     'row_2_color': Color(.1, .1, .1, 0.2)
    # }

    def __init__(self, inventory_object, **kwargs):
        '''Get the information from the saved inventory object to put into the label widgets'''
        self.object = inventory_object
        self.UID = self.object.UID

        super(ContainerDataRow, self).__init__(**kwargs)
        self.__initLog__('rows_inventory.py', 'ContainerDataRow')
        self.logDebug('Creating a ContainerDataRow instance')

        self.usd_value_col_width = 65
        self.weight_col_width = 45

        self.assignValues()

        self.object.widget = self

    def __repr__(self):
        s = \
        f'<<ContainerDataRow widget for {self.object.description} with parent widget: {self.parent}>>'
        return s

    def assignValues(self):
        self.logDebug(f'Assigning data from {self.object}')

        self.obj_label.text = str(self.object.description)
        self.val_label.text = str(self.object.usd_value)
        self.loc_label.text = 'Home'
        self.weight_label.text = str(self.object.weight)
