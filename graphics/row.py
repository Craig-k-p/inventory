from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.properties import BooleanProperty
from resources.utilities import LogMethods


class DataRow():
    def deselect(self):
        self.selected = False
    def select(self):
        self.selected = True
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



    def setBounds(self):
        # the to_window method gets the coordinates according to the window
        # instead of according to the parent widget
        self.xy = self.pos
        self.x0 = self.xy[0]
        self.x1 = self.xy[0] + self.width
        self.y0 = self.xy[1]
        self.y1 = self.xy[1] + self.height
        self.bounds = (self.x0, self.x1, self.y0, self.y1)
        # self.logDebug(f'Set {self.object.description}\'s boundaries: {self.getBounds()}')

    def wasClicked(self, touch):
        '''Check if this widget was clicked using the click/touch coordinates and the
           self.x0y0 (etc) bounds'''

        x, y = touch.pos[0], touch.pos[1]
        if self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1:
            # self.logDebug(f'{self.object.description} was clicked')
            return True
        else:
            # self.logDebug(f'{self.object.description} was not clicked')
            return False


class ContainerHeadingRow(GridLayout, LogMethods):
    container = ObjectProperty(None)
    weight = ObjectProperty(None)
    val = ObjectProperty(None)
    my_text = StringProperty(None)

    settings = {
        'heading_color': Color(.1, .1, .1, 0.2)
    }

    def __init__(self, **kwargs):
        super(ContainerHeadingRow, self).__init__(**kwargs)
        self.__initLog__('rows_inventory.py', 'ContainerHeadingRow')

        # self.logDebug('Creating a ContainerHeadingRow instance')

    def setHeadingText(self,
                       container='Container',
                       weight='LBS',
                       usd_value='$$',
                       options='Opts'
                       ):
        '''Set the heading text for each child widget Label'''
        # log = f'Setting heading Label text values to {container}, {weight}, {usd_value}, '
        # log += f'and {options}'
        # self.logDebug(log)
        # self.logDebug(f'self.weight.label = {self.weight_label.text}')

        self.obj_label.text = 'HELP'
        self.weight_label.text = weight
        self.val_label.text = self.my_text
        self.opt_button.text = options

        self.logDebug(f'container.label = {self.obj_label.text}')

        log = f'Values: {self.obj_label.text}, {self.weight_label.text}, {self.val_label.text}'
        self.logDebug(log)


class ContainerDataRow(GridLayout, DataRow, LogMethods):
    obj_label = ObjectProperty(None)
    weight_label = ObjectProperty(None)
    val_label = ObjectProperty(None)
    selected = BooleanProperty(False)

    def __init__(self, inventory_object, **kwargs):
        '''Get the information from the saved inventory object to put into the label widgets'''
        self.object = inventory_object
        self.ID = self.object.ID

        super(ContainerDataRow, self).__init__(**kwargs)
        self.__initLog__('rows_inventory.py', 'ContainerDataRow')
        # self.logDebug('Creating a ContainerDataRow instance')

        self.object.widget = self

        self.assignValues()

    def __repr__(self):
        s = f'<<ContainerDataRow widget for {self.object.description} with parent '
        s += f'widget: {self.parent}>>'
        return s

    def assignValues(self):
        self.obj_label.text = str(self.object.description)
        self.val_label.text = self.formatValue(self.object.getValue())
        self.weight_label.text = self.formatWeight(self.object.getWeight())

        # self.logDebug(f'got values: {self.weight_label.text} lbs, ${self.val_label.text}')


class ThingHeadingRow(GridLayout, LogMethods):
    obj_label = ObjectProperty(None)
    weight_label = ObjectProperty(None)
    val_label = ObjectProperty(None)
    opt_label = ObjectProperty(None)

    settings = {
        'heading_color': Color(.1, .1, .1, 0.2)
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__initLog__('rows_box.py', 'ThingHeadingRow')

        # self.logDebug('Creating a ThingHeadingRow instance..')

    def setHeadingText(self,
                       container='Thing',
                       weight='LBs',
                       usd_value='$$',
                       options='Opts'
                       ):
        '''Set the heading text for each child widget Label'''
        log = f'Setting heading Label text values to {container}, {weight}, {usd_value},'
        log += f'and {options}'
        self.logDebug(log)

        self.obj_label.text = 'HELP'
        self.weight_label.text = weight
        self.val_label.text = self.my_text
        self.opt_button.text = options


class ThingDataRow(GridLayout, DataRow, LogMethods):

    obj_label = ObjectProperty(None)
    weight_label = ObjectProperty(None)
    val_label = ObjectProperty(None)
    selected = BooleanProperty(False)

    def __init__(self, inventory_object, **kwargs):
        '''Get the information from database to put into the label widgets'''
        self.object = inventory_object
        self.ID = self.object.ID

        super(ThingDataRow, self).__init__(**kwargs)
        self.__initLog__('rows_thing.py', 'ThingDataRow')
        # self.logDebug('Creating a ThingDataRow instance')

        # self.logDebug(f'self.object = {self.object}')

        self.object.widget = self

        self.assignValues()

    def __repr__(self):
        s = f'<<ThingDataRow widget for {self.object.description} with parent widget:'
        s += f' {self.parent}>>'
        return s

    def assignValues(self):
        '''Update/assign the widgets' text values'''

        self.obj_label.text = str(self.object.description)
        self.val_label.text = self.formatValue(self.object.usd_value)
        self.weight_label.text = self.formatWeight(self.object.weight)

        # self.logDebug(f'Assigning data from {self.object}')
