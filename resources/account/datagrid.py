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

        self.logInfo('kv_ops', f'Creating DataGrid instance')

        # Colors for each row
        self.heading_color = None
        self.row_1_color = None
        self.row_2_color = None

        # Unique ids for each data row
        self.UIDs = 0

        # Store the InventoryDataRow instances here
        self.dataRows = {}

    def addDataRow(self):
        '''Add a row of fields to the GridLayout with the given data
        Future:
            -tie each dataRow to it's actual container/thing object data from the server
            -tie into database functionality
        '''
        UID = self._getUID()

        self.logDebug('kv_ops', f'Adding row {UID}..')

        new_row = self.getDataRowClass()(UID)
        self.dataRows[UID] = new_row
        self.add_widget(self.dataRows[UID])

    def removeDataRow(self, UID):
        '''Remove a row of fields from the GridLayout
        Future:
            -confirm?
            -delete associated row with click
            -tie into database functionality
        '''
        self.logDebug('kv_ops', f'Removing row {UID}..')
        self.remove_widget(self.dataRows.pop(UID))

    def setObjectCategory(self, category):
        '''Set the category of object that this grid will be dealing with - ie "containers" or "things" -
           which will allow the instance to check which type of row/heading it will be instantiating'''

        self.logDebug('kvLogic', f'Setting the DataGrid category to {category}')

        if category in DataGrid.categories:
            category = category
        else:
            self.logCritical('kvLogic', f'category was {category}, not "things" or "containers."  Expect failures')
            raise Exception(f'self.category must be "things" or "containers", not {category}')

        self.logDebug('kvLogic', 'Assigning references to the approprate classes..')
        # Set references to the proper classes for this instance
        if category == 'things':
            self._HeadingCls = BoxHeadingRow
            self._DataRowCls = BoxDataRow
        elif category == 'containers':
            self._HeadingCls = InventoryHeadingRow
            self._DataRowCls = InventoryDataRow

        self.logDebug('kvLogic', 'Creating the heading row..')

        # Create the heading widgets used to label the top of the data fields
        self.headings = self.getHeadingClass()()
        self.add_widget(self.headings)

    def _assignColumnWidths(self):
        '''Loop thru each child widget that needs a fixed width and set its width.  This
           makes sure that each row has a uniform width.
        Comments:
            Not working.  Recieving 0 and 10 for x and y not matter the actual size
        Future maybe's:
            -Set the column width to the minimum needed width to fit the values
           '''

        self.logInfo('kv_ops', 'Assigning column widths')

        for row in self.dataRows:
            tex_width = self.dataRows[row].val_lo.width
            self.logDebug('kvLogic', f'Label size: {tex_width}')
            # tex_width = row.val_lo.texture_size
            # self.logDebug('kvLogic', f'Label size: {tex_width}')

    def getDataRowClass(self):

        self.logInfo('kv_ops', f'Returning self._DataRowCls: {self._DataRowCls}')
        return self._DataRowCls

    def getHeadingClass(self):
        self.logInfo('kv_ops', f'Returning self._HeadingCls: {self._HeadingCls}')
        return self._HeadingCls

    def _getUID(self):
        '''Increment self.UIDs and return the value'''

        self.UIDs += 1
        self.logInfo('kvLogic', f'Incremented self.UID to {self.UIDs}')
        return self.UIDs

    def _getMaxWidth(self):
        '''Loop thru each child widget's children and get the maximum width needed for the column'''

    def TestRandomPopulate(self):
        '''Populate the rows with random data'''

        self.logDebug('kv_ops', 'Randomly populating rows')

        # Add some data rows for testing
        for n in range(1, random.randint(3, 20)):
            # Get the row ID
            UID = self._getUID()
            # Create the row instance
            row = self.getDataRowClass()(UID)

            # Add the row to the dictionary
            self.dataRows[UID] = row

        # self._assignColumnWidths()

        # Add them to the screen to be drawn
        for data in self.dataRows:
            self.add_widget(self.dataRows[data])
