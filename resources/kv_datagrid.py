import pprint
import random

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.graphics.instructions import InstructionGroup
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from resources.utilities import WindowKeyboard, LogMethods


''' REDO

Make a Row class and add it to the GridLayout as needed.  Keep track of instances, add/change variables with
objectproperties, etc.




'''


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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__initLog__(
            'kv_DG.py',
            'InventoryHeadingRow'
        )
        # self.my_text = '$$'

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

    def __init__(self, UID, **kwargs):
        '''Get the information from database to put into the label widgets'''
        super().__init__(**kwargs)
        # self.data = data
        self.__initLog__(
            'kv_DG.py',
            'InvDataRow'
        )

        self.UID = UID

        self.value_col_width = 70
        self.weight_col_width = 50

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
        self.val_label.text = f'{random.randint(0,99)}.{random.randint(10,99)}'
        self.weight_label.text = f'{random.randint(0,99)}.{random.randint(0,9)}'


class DataGrid(GridLayout, WindowKeyboard, LogMethods):

    def __init__(self, **kwargs):
        '''Creates the widgets in a user-defined manner'''
        # Init the parent, ScrollView
        super().__init__(**kwargs)
        # Setup the logger
        self.__initLog__(
            file_str='kv_DG.py',
            class_str='DataGrid'
        )

        self.logInfo('kv_ops', f'Creating DataGrid instance')

        self.UIDs = 0

        # Create the heading widgets used to label the top of the data fields
        self.headings = InventoryHeadingRow()
        self.add_widget(self.headings)

        # Store the InventoryDataRow instances here
        self.dataRows = {}

        # Add some data rows for testing
        for n in range(1, 7):
            # Get the row ID
            UID = self._getUID()
            # Create the row instance
            row = InventoryDataRow(UID)

            # Add the row to the dictionary
            self.dataRows[UID] = row

        self._assignColumnWidths()

        # Add them to the screen to be drawn
        for data in self.dataRows:
            self.add_widget(self.dataRows[data])

        # Lists of widgets for each row, in order
        # self.rows = {}

        # # Make sure we can reference needed class attributes like DataGric.row_2_color
        # if DataGrid.row_1_color is None or DataGrid.row_2_color is None or DataGrid.heading_color is None:
        #     self.logDebug('kv_ops', 'Initializing DataGrid.heading_color, .row_1_color, and .row_2_color...')
        #     DataGrid.heading_color = InstructionGroup()
        #     DataGrid.heading_color.add(Color(.1, .1, .1, 0.2))
        #     DataGrid.heading_color.add(Rectangle(pos=self.pos, size=self.size))

        #     DataGrid.row_1_color = InstructionGroup()
        #     DataGrid.row_1_color.add(Color(.1, .1, .1, 1))
        #     DataGrid.row_1_color.add(Rectangle(pos=self.pos, size=self.size))

        #     DataGrid.row_2_color = InstructionGroup()
        #     DataGrid.row_2_color.add(Color(.1, .1, .1, 0.7))
        #     DataGrid.row_2_color.add(Rectangle(pos=self.pos, size=self.size))

        #     # Here, self should be a Widget or subclass
        #     # [self.canvas.add(group) for group in [blue, green]]

        # else:
        #     self.logDebug('kv_ops', 'DataGrid.heading_color, .row_1_color, and .row_2_color exist already')

        # self._createHeadings()

    def addDataRow(self):
        '''Add a row of fields to the GridLayout with the given data
        Future:
            -tie each dataRow to it's actual container object
            -tie into database functionality
        '''
        UID = self._getUID()
        new_row = InventoryDataRow(UID)
        self.dataRows[UID] = new_row
        self.add_widget(self.dataRows[UID])

    def removeDataRow(self, UID):
        '''Remove a row of fields from the GridLayout
        Future:
            -confirm?
            -delete associated row with click
            -tie into database functionality
        '''
        self.remove_widget(self.dataRows.pop(UID))

    def _assignColumnWidths(self):
        '''Loop thru each child widget that needs a fixed width and set its width.  This
           makes sure that each row has a uniform width.
        Comments:
            Not working.  Recieving 0 and 10 for x and y not matter the actual size
        Future maybe's:
            -Set the column width to the minimum needed width to fit the values
           '''
        for row in self.dataRows:
            tex_width = self.dataRows[row].val_lo.width
            self.logDebug('kvLogic', f'Label size: {tex_width}')
            # tex_width = row.val_lo.texture_size
            # self.logDebug('kvLogic', f'Label size: {tex_width}')

    def _createHeadings(self):
        '''Loop through the data dict and create some heading widgets, starting with an AnchorLayout and 
           finishing with a Label as a child.
        Future:
            -To be removed
        '''
        self.logDebug('kv_ops', 'Creating headings')

        # Add the canvas grpahics instructions to the anchor
        self.headings[get_col].canvas.add(DataGrid.heading_color)

        self.logDebug('kv_ops'), f'Creating Label for {get_col} column'
        # Get the options for the Label
        title = get_col
        c = self.app.kv_settings['text color']
        sh = self.data[get_col]['label']['draw']['size_hint']
        # Texture size after instanciationn

        # Instanciate a Label widget
        self.headings[get_col]['label'] = Label(
            text=title,
            color=c,
            size_hint=sh)
        # Set the size of the Label's borders to match that of the text texture image (plus some x padding)
        self.headings[get_col]['label'].size = (
            self.headings[get_col]['label'].texture_size[0] + 10,
            self.headings[get_col]['label'].texture_size[1]
        )

    def _formatFields(self):
        pass

    def _getUID(self):
        '''Increment self.UIDs and return the value'''
        self.UIDs += 1
        return self.UIDs

    def _setDataDictDefaults(self):
        '''Go through the provided dictionary and set default values if none are found'''

    def _getMaxWidth(self):
        '''Loop thru each child widget's children and get the maximum width needed for the column'''
