import random

from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from resources.utilities import LogMethods, WindowKeyboard


class InventoryHeadingRow(GridLayout, LogMethods):
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
            'InventoryHeadingRow'
        )

        self.logDebug('kv_ops', 'Creating an InventoryHeadingRow instance')

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
        self.logDebug('kvLogic', log)
        # self.logDebug('kvLogic', f'container.label = {self.container.label}')
        self.logDebug('kvLogic', f'self.weight.label = {self.weight_label.text}')

        self.obj_label.text = 'HELP'
        self.weight_label.text = weight
        self.val_label.text = self.my_text
        self.loc_label.text = location
        self.tag_button.text = tags
        self.opt_button.text = options

        self.logDebug('kvLogic', f'container.label = {self.obj_label.text}')

        log = f'Values: {self.obj_label.text}, {self.weight_label.text}, {self.val_label.text}'
        self.logDebug('kvLogic', log)


class InventoryDataRow(GridLayout, WindowKeyboard, LogMethods):

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

    def __init__(self, UID, **kwargs):
        '''Get the information from database to put into the label widgets'''
        super().__init__(**kwargs)
        # self.data = data
        self.__initLog__(
            'rows_inventory.py',
            'InvDataRow'
        )

        self.logDebug('kv_ops', 'Creating an InvDataRow instance')

        self.UID = UID

        self.value_col_width = 65
        self.weight_col_width = 45

        self.choices = ['ice cream', 'coffee', 'turnips', 'beans', 'lice', 'panzerfaust', 'crossiant']
        self.locations = ['home', 'cabin', 'bottom of the lake', 'New York', 'gf house', 'grandmas house']
        self.randomValues()

    def randomValues(self):
        '''Set the heading text for each child widget Label'''

        objs = [self.obj_label, self.loc_label]

        # Choose a random string value for the text attribute
        for obj in objs:
            obj.text = random.choice(self.choices)

        self.obj_label.text = random.choice(self.choices)
        self.loc_label.text = random.choice(self.locations)
        self.val_label.text = f'{random.randint(0,4000)}.{random.randint(10,99)}'
        self.weight_label.text = f'{random.randint(0,199)}.{random.randint(0,9)}'
