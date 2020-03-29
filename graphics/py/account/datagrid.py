from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.graphics.instructions import InstructionGroup
from kivy.properties import ObjectProperty, StringProperty, NumericProperty

from resources.utilities import LogMethods
from graphics.py.account.rows_container import ContainerHeadingRow, ContainerDataRow
from graphics.py.account.rows_thing import ThingHeadingRow, ThingDataRow

from json import dumps


class DataGrid(GridLayout, LogMethods):

    categories = ('Container', 'Thing')

    # Store the ContainerDataRow instances here
    dataRows = {'containers': {}, 'things': {}}

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
        self.logInfo('--TESTING--', f'self.parent: {self.parent}')

        self.app = None

        # Colors for each row
        self.heading_color = None
        self.row_1_color = None
        self.row_2_color = None

    def addDataRow(self, object_doc):
        '''Add a row of fields to the GridLayout with the given data
        Future:
            -DONE tie each dataRow to it's actual container/thing object data from the server
            -tie into database functionality
        '''

        if self.app == None:
            # Allow easy access to the app instance for IO calls
            self.app = self.parent.parent.parent.parent.app

        self.logDebug('Kv Ops', 'Adding a new data row to the DataGrid instance')
        # Get a unique ID for the row
        UID = self.app._getUID()

        self.logDebug('kv_ops', f'UID: {UID}')

        # Instantiate a data row with UID and document
        new_row = self.getDataRowClass()
        self.logDebug('kv_ops', f'new_row: {new_row}')
        self.logDebug('kv_ops', f'UID: {UID}')
        self.logDebug('kv_ops', f'object_doc: {object_doc}')
        new_row = new_row(UID, object_doc)

        # Add the ***DataRow instance to the dataRows dictionary and link it to IOHandler instance
        self.dataRows[UID] = {
            'row': new_row,
            'doc': object_doc
        }
        # Link to the appropriate dictionary in iohandler.py
        if self.category == 'Thing':
            self.app.things = self.dataRows
        elif self.category == 'Container':
            self.app.containers = self.dataRows

        self.logDebug('TEST', f'self.dataRows: {self.dataRows}')

        self.logDebug('Kv Ops', f'Adding the row for {object_doc["description"]} to the grid')
        # Add the ***DataRow instance to the DataGrid widget
        self.add_widget(self.dataRows[UID]['row'])

        self.logDebug('TEST', f' {self.app}')


    def fillUserData(self, app):
        ''' Populate the rows with user data '''

        # Get access to the application instance
        if self.app == None:
            self.app = app
        # # Try to load data if it hasn't already been loaded
        # if self.app.load_data == None:
        #     self.app.loadData()

        self.logDebug('Db Logic', f'Getting data for the data grid in category {self.category}')
        # Get the containers or things to fill the data grid
        data = self.app.getObjects(self.category)

        # {'1': {
        #     'description': 'asdf',
        #     'usd_value': '3',
        #     'weight': '3'}}

        self.logInfo('KV Logic', f'Data:\n{dumps(data, indent=4)}')

        if self.getDataRowClass() == 'Container':
            data_class = 'containers'
        else:
            data_class = 'things'

        self.logDebug('Db Logic', 'Looping thru the data')
        for key in data:
            # Get a row ID
            UID = self.app._getUID()

            self.logDebug('KV Logic', f'data[key]:\n{dumps(data[key], indent=4)}')

            # Create the ContainerDataRow or ThingDataRow instance
            row = self.getDataRowClass()(UID, data[key])

            # Add it to the dictionary
            self.dataRows[UID] = row

        # Add the rows to the screen to be drawn
        for drow in self.dataRows:
            self.add_widget(self.dataRows[drow])

    def getDataRowClass(self):
        ''' Return a reference to ContainerDataRow or ThingDataRow class def'''
        self.logInfo('kv_ops', f'Returning self._DataRowCls: {self._DataRowCls}')
        return self._DataRowCls

    def getHeadingClass(self):
        ''' Return a reference to ****HeadingRow class def '''
        self.logInfo('kv_ops', f'Returning self._HeadingCls: {self._HeadingCls}')
        return self._HeadingCls

    def removeDataRow(self, UID):
        '''Remove a row of fields from the GridLayout'''
        self.logDebug('kv_ops', f'Removing row {UID}..')
        self.remove_widget(self.dataRows.pop(UID))

    def setObjectCategory(self, category):
        '''Set the category of object that this grid will be dealing with - ie "containers" or
           "things" - which will allow the instance to check which type of row/heading it will
           be instantiating
           Called in screens.py'''

        self.logDebug('kvLogic', f'Setting the DataGrid category to {category}')

        # Make sure the category is valid
        if category in DataGrid.categories:
            self.category = category
        else:
            self.logCritical(
                'kvLogic',
                f'category was {category}, not "things" or "containers."  Expect failures'
            )
            raise Exception(f'self.category must be "things" or "containers", not {category}')

        self.logDebug('kvLogic', 'Assigning references to the approprate classes..')

        # Set references to the proper classes for this instance
        if self.category == 'Thing':
            self._HeadingCls = ThingHeadingRow
            self._DataRowCls = ThingDataRow
            # Link the correct dictionary stored in DataGrid.dataRows for storing row instances
            self.dataRows = DataGrid.dataRows['things']

        elif self.category == 'Container':
            self._HeadingCls = ContainerHeadingRow
            self._DataRowCls = ContainerDataRow
            # Link the correct dictionary stored in DataGrid.dataRows for storing row instances
            self.dataRows = DataGrid.dataRows['containers']

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

    def _getMaxWidth(self):
        '''Loop thru each child widget's children and get the maximum width needed for the
        column'''
        self.logInfo('kvLogic', f'Did nothing...')
