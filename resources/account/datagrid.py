import pprint
import random

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.graphics.instructions import InstructionGroup
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from resources.utilities import WindowKeyboard, LogMethods
from resources.account.rows_inventory import InventoryHeadingRow, InventoryDataRow
from resources.account.rows_box import BoxHeadingRow, BoxDataRow


''' REDO

Make a Row class and add it to the GridLayout as needed.  Keep track of instances, add/change variables with
objectproperties, etc.




'''


class DataGrid(GridLayout, WindowKeyboard, LogMethods):

    categories = ('containers', 'things')

    def __init__(self, **kwargs):
        '''Creates the widgets in a user-defined manner'''
        # Init the parent, ScrollView
        super().__init__(**kwargs)
        # Setup the logger
        self.__initLog__(
            file_str='kv_DG.py',
            class_str='DataGrid'
        )

        self.heading_color = None
        self.row_1_color = None
        self.row_2_color = None

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

        # # Make sure we can reference needed class attributes like DataGrid.row_2_color
        # if DataGrid.row_1_color is None or DataGrid.row_2_color is None or DataGrid.heading_color is None:
        #     self.logDebug('kv_ops', 'Initializing DataGrid.heading_color, .row_1_color, and .row_2_color...')
        #     DataGrid.heading_color = InstructionGroup()
        #     DataGrid.heading_color.add(Color(.1, .1, .1, 0.2))
        #     DataGrid.heading_color.add(Rectangle(pos=self.pos, size=self.size))

        #     DataGrid.row_1_color = InstructionGroup()
        #     DataGrid.row_1_color.add(Color(.1, .1, .1, 1))
        #     DataGrid.row_1_color.add(Rectangle(pos=self.pos, size=self.size))

    def addDataRow(self):
        '''Add a row of fields to the GridLayout with the given data
        Future:
            -tie each dataRow to it's actual container/thing object
            -tie into database functionality
        '''
        UID = self._getUID()

        if self.category == 'containers':
            new_row = InventoryDataRow(UID)
        elif self.category == 'things':
            new_row = BoxDataRow(UID)
        else:
            log = f'User attempted to addDataRow(), but self.category was {self.category}, '
            log += 'not "containers" or "things"'
            self.logError('kv_ops', log)
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

    def _getUID(self):
        '''Increment self.UIDs and return the value'''
        self.UIDs += 1
        return self.UIDs

    def setObjectCategory(self, category):
        '''Set the category of object that this grid will be dealing with - ie "containers" or "things" -
           which will allow the instance to check which type of row/heading it will be instantiating'''
        if category in DataGrid.categories:
            self.category = category
        else:
            self.logCritical('kvLogic', f'category was {category}, not "things" or "containers."  Expect failures')

    def _getMaxWidth(self):
        '''Loop thru each child widget's children and get the maximum width needed for the column'''
