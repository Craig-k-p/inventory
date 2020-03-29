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
        super().__init__(**kwargs)
        self.__initLog__(
            'rows_inventory.py',
            'ContainerHeadingRow'
        )

        self.logDebug('kv Ops', 'Creating an ContainerHeadingRow instance')

    def setHeadingText(self,
                       container='Container',
                       weight='LBS',
                       value='$$',
                       location='Location',
                       tags='Tags',
                       options='Opts'
                       ):
        '''Set the heading text for each child widget Label'''
        log = f'Setting heading Label text values to {container}, {weight}, {value}, '
        log += f'{location}, {tags}, and {options}'
        self.logDebug('kv Logic', log)
        self.logDebug('kv Logic', f'self.weight.label = {self.weight_label.text}')

        self.obj_label.text = 'HELP'
        self.weight_label.text = weight
        self.val_label.text = self.my_text
        self.loc_label.text = location
        self.tag_button.text = tags
        self.opt_button.text = options

        self.logDebug('kv Logic', f'container.label = {self.obj_label.text}')

        log = f'Values: {self.obj_label.text}, {self.weight_label.text}, {self.val_label.text}'
        self.logDebug('kv Logic', log)


class ContainerDataRow(GridLayout, LogMethods):

    obj_label = ObjectProperty(None)
    weight_label = ObjectProperty(None)
    val_label = ObjectProperty(None)
    loc_label = ObjectProperty(None)
    tag_button = ObjectProperty(None)
    opt_button = ObjectProperty(None)
    weight_col_width = NumericProperty(50)
    val_col_width = NumericProperty(65)

    settings = {
        'row_1_color': Color(.1, .1, .1, 0.2),
        'row_2_color': Color(.1, .1, .1, 0.2)
    }

    def __init__(self, UID, object_doc, **kwargs):
        '''Get the information from database to put into the label widgets'''
        super().__init__(**kwargs)
        # self.data = data
        self.__initLog__(
            'rows_inventory.py',
            'ContainerDataRow'
        )

        self.logDebug('kv Ops', 'Creating a ContainerDataRow instance')

        self.UID = UID
        self.object_doc = object_doc

        self.value_col_width = 65
        self.weight_col_width = 45

        self.choices = ['ice cream', 'coffee', 'turnips', 'beans', 'lice', 'panzerfaust', 'crossiant']
        self.locations = ['home', 'cabin', 'bottom of the lake', 'New York', 'gf house', 'grandmas house']
        self.assignValues()

    def assignValues(self):
        self.logDebug('KV Logic', f'self.object_doc: {self.object_doc}')
        self.logDebug(
            'KV Logic',
            f'{self.object_doc["description"]}, {self.object_doc["usd_value"]}, {self.object_doc["weight"]}'
            )

        self.obj_label.text = str(self.object_doc["description"])
        self.loc_label.text = 'Home'
        self.val_label.text = str(self.object_doc["usd_value"])
        self.weight_label.text = str(self.object_doc["weight"])
