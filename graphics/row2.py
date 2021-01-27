from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from resources.utilities import LogMethods


class HeadingRow(GridLayout, LogMethods):
    item = ObjectProperty(None)
    weight = ObjectProperty(None)
    val = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(HeadingRow, self).__init__(**kwargs)
        self.__initLog__('rows_inventory.py', 'ContainerHeadingRow')


class DataRow(GridLayout, LogMethods):
    obj_label = ObjectProperty(None)
    weight_label = ObjectProperty(None)
    val_label = ObjectProperty(None)
    selected = BooleanProperty(False)

    def __init__(self, inventory, **kwargs):
        '''Get the information from the saved inventory object to put into the label widgets'''
        self.inventory = inventory

        super(DataRow, self).__init__(**kwargs)
        self.__initLog__('rows_inventory.py', 'ContainerDataRow')
        self.logDebug('Creating a ContainerDataRow instance')

        self.assignValues()

    def __repr__(self):
        s = f'<DataRow for {self.inventory.description}>'
        return s

    def assignValues(self):
        self.obj_label.text = str(self.inventory.description)
        self.val_label.text = self.formatValue(self.inventory.usd_value)
        self.weight_label.text = self.formatWeight(self.inventory.weight)

    def deselect(self):
        self.selected = False
    def getBounds(self):
        return self.bounds

    def formatValue(self, obj_value, value_symbol='$'):
        value = round(float(obj_value), 2)
        dollars, cents = str(value).split('.')

        if value > 9999:
            return f"{value_symbol}{format(int(dollars), ',.0f')}"

        # Make sure cents are 2 decimal places
        if len(cents) == 0:
            cents = '.00'
        elif len(cents) == 1:
            cents = f'.{cents}0'

        value = float(f'{dollars}{cents}')

        if 0 <= value:
            return f"{value_symbol}{format(value, ',.2f')}"

        else:
            return f"-{value_symbol}{format(abs(value), ',.2f')}"

    def formatWeight(self, obj_weight, weight_symbol='lbs'):
        weight = round(float(obj_weight), 1)
        whole_number, decimal = str(weight).split('.')

        if len(decimal) == 0 or decimal == '0':
            return f'{whole_number} {weight_symbol}'

        weight = float(f'{whole_number}.{decimal}')

        if 0 <= weight < 100:
            return f"{format(weight, ',.1f')} {weight_symbol}"
        else:
            return f'{whole_number} {weight_symbol}'

    def select(self):
        self.selected = True

    def setBounds(self):
        # the to_window method gets the coordinates according to the window
        # instead of according to the parent widget
        self.xy = self.pos
        self.x0 = self.xy[0]
        self.x1 = self.xy[0] + self.width
        self.y0 = self.xy[1]
        self.y1 = self.xy[1] + self.height
        self.bounds = (self.x0, self.x1, self.y0, self.y1)
        # self.logDebug(f'Set {self.inventory.description}\'s boundaries: {self.getBounds()}')

    def wasClicked(self, touch):
        '''Check if this widget was clicked using the click/touch coordinates and the
           self.x0y0 (etc) bounds'''

        x, y = touch.pos[0], touch.pos[1]
        if self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1:
            # self.logDebug(f'{self.inventory.description} was clicked')
            return True
        else:
            # self.logDebug(f'{self.inventory.description} was not clicked')
            return False
