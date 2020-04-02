import random

from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from resources.utilities import LogMethods

# Try something like this for colors
# # Make sure we can reference needed class attributes like DataGrid.row_2_color
# if DataGrid.row_1_color is None or DataGrid.row_2_color is None or DataGrid.heading_color is None:
#     self.logDebug('kv_ops', 'Initializing DataGrid.heading_color, .row_1_color, and .row_2_color...')
#     DataGrid.heading_color = InstructionGroup()
#     DataGrid.heading_color.add(Color(.1, .1, .1, 0.2))
#     DataGrid.heading_color.add(Rectangle(pos=self.pos, size=self.size))

#     DataGrid.row_1_color = InstructionGroup()
#     DataGrid.row_1_color.add(Color(.1, .1, .1, 1))
#     DataGrid.row_1_color.add(Rectangle(pos=self.pos, size=self.size))


class ThingHeadingRow(GridLayout, LogMethods):
    obj_label = ObjectProperty(None)
    weight_label = ObjectProperty(None)
    val_label = ObjectProperty(None)
    tag_label = ObjectProperty(None)
    opt_label = ObjectProperty(None)
    # my_text = StringProperty(None)
    weight_col_width = NumericProperty(50)
    val_col_width = NumericProperty(65)

    settings = {
        'heading_color': Color(.1, .1, .1, 0.2)
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__initLog__(
            'rows_box.py',
            'ThingHeadingRow'
        )

        self.logDebug('Creating a ThingHeadingRow instance..')

    def setHeadingText(self,
                       container='Thing',
                       weight='LBs',
                       value='$$',
                       tags='Tags',
                       options='Opts'
                       ):
        '''Set the heading text for each child widget Label'''
        log = f'Setting heading Label text values to {container}, {weight}, {value}, '
        log += f'{tags}, and {options}'
        self.logDebug(log)

        self.obj_label.text = 'HELP'
        self.weight_label.text = weight
        self.val_label.text = self.my_text
        self.tag_button.text = tags
        self.opt_button.text = options


class ThingDataRow(GridLayout, LogMethods):

    obj_label = ObjectProperty(None)
    weight_label = ObjectProperty(None)
    val_label = ObjectProperty(None)
    tag_button = ObjectProperty(None)
    opt_button = ObjectProperty(None)
    weight_col_width = NumericProperty(50)
    val_col_width = NumericProperty(65)

    # settings = {
    #     'row_1_color': Color(.1, .1, .1, 0.2),
    #     'row_2_color': Color(.1, .1, .1, 0.2)
    # }

    def __init__(self, inventory_object, **kwargs):
        '''Get the information from database to put into the label widgets'''
        self.object = inventory_object
        self.object.widget = self
        self.UID = self.object.UID

        super(ThingDataRow, self).__init__(**kwargs)
        self.__initLog__('rows_thing.py', 'ThingDataRow')
        self.logDebug('Creating a ThingDataRow instance')

        self.value_col_width = 65
        self.weight_col_width = 40

        self.assignValues()

    def __repr__(self):
        s = \
        f'<<ThingDataRow widget for {self.object} with parent widget: {self.parent}>>'
        return s

    def assignValues(self):
        self.logDebug(f'Assigning data from {self.object}')

        self.obj_label.text = str(self.object.description)
        self.val_label.text = str(self.object.value)
        self.weight_label.text = str(self.object.weight)
