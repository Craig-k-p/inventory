import pprint

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.graphics.instructions import InstructionGroup
from kivy.properties import ObjectProperty, StringProperty
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__initLog__(
            'kv_DG.py',
            'InventoryHeadingRow'
        )
        self.my_text = '$$'

    def setHeadingText(self,
                       container='Container',
                       weight='LBS',
                       value='$$',
                       location='Location',
                       tags='Tags',
                       options='Opts'
                       ):
        '''Set the heading text for each child widget Label'''
        log = f'Setting heading Label text values to {container}, {weight}, {value}, {location}, {tags}, and {options}'
        self.logDebug('kvLogic', log)
        # self.logDebug('kvLogic', f'container.label = {self.container.label}')
        self.logDebug('kvLogic', f'self.weight.label = {self.weight.label}')

        self.container.label.text = 'HELP'
        self.weight.label.text = weight
        self.val.label.text = self.my_text
        self.loc.label.text = location
        self.tag.button.text = tags
        self.opt.button.text = options

        self.logDebug('kvLogic', f'container.label = {self.container.label.text}')

        log = f'Values: {self.container.label.text}, {self.weight.label.text}, {self.val.label.text}'
        self.logDebug('kvLogic', log)


class InventoryDataRow(GridLayout, WindowKeyboard, LogMethods):

    obj = ObjectProperty(None)
    weight = ObjectProperty(None)
    val = ObjectProperty(None)
    loc = ObjectProperty(None)
    tag_but = ObjectProperty(None)
    opt_but = ObjectProperty(None)

    def __init__(self, **kwargs):
        '''Get the information from database to put into the label widgets'''
        super().__init__(**kwargs)
        # self.data = data


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
        print(__file__)

        # self.logInfo('kv_ops', f'Creating DataGrid instance {title}...')
        # Create reference to the app
        # self.app = app

        # Title for this "spreadsheet" of information
        # self.title = title

        # Create the heading widgets used to label the top of the data fields
        self.headings = InventoryHeadingRow()
        # Assign heading text
        self.headings.setHeadingText()
        self.add_widget(self.headings)

        self.dataRows = []
        self.dataRows.append(InventoryDataRow())

        for data in self.dataRows:
            self.add_widget(data)

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

    def addDataRow(self, data):
        '''Add a row of fields to the GridLayout with the given data'''

    def removeDataFields(self, field):
        '''Remove a row of fields from the GridLayout'''

    def _assignMaxWidth(self):
        '''Loop thru each child widget that needs a fixed width and set its width'''

    def _createHeadings(self):
        '''Loop through the data dict and create some heading widgets, starting with an AnchorLayout and finishing with
           a Label as a child.'''

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

    def _setDataDictDefaults(self):
        '''Go through the provided dictionary and set default values if none are found'''

    def _getMaxWidth(self):
        '''Loop thru each child widget's children and get the maximum width needed for the column'''
