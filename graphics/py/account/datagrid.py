from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.graphics.instructions import InstructionGroup
from kivy.properties import ObjectProperty, StringProperty, NumericProperty

from resources.utilities import LogMethods
from resources.inventoryobjects import Thing, Container, InventoryObject
from graphics.py.account.rows_container import ContainerHeadingRow, ContainerDataRow
from graphics.py.account.rows_thing import ThingHeadingRow, ThingDataRow

from json import dumps


class DataGrid(GridLayout, LogMethods):

    categories = ('container', 'thing')

    # # Store the ContainerDataRow instances here
    # dataRows = {'containers': {}, 'things': {}}

    def __init__(self, **kwargs):
        '''Creates the widgets in a user-defined manner'''
        # Init the parent, ScrollView
        super().__init__(**kwargs)
        # Setup the logger
        self.__initLog__(file_str='kv_DG.py', class_str='DataGrid')

        self.logInfo('Creating DataGrid instance')

        self.app = None

        self.heading_color = None
        self.row_1_color = None
        self.row_2_color = None

        self.category = None

    def __repr__(self):
        s = f'<<{self.category} DataGrid>>'
        return s

    def addDataRow(self, inventory_object):
        '''Add a row of fields to the GridLayout with the given data
           data is a dict of user input'''

        if self.app == None:
            # Allow easy access to the app instance for IO calls
            self.app = self.parent.parent.parent.parent.app
        # if self.inventory_kv == {}:
        #     self.inventory_kv = self.app.inventory_kv
        # if self.inventory == None:
        #     self.inventory = self.app.inventory

        self.logDebug(f'Creating a widget for {inventory_object}')

        # Instantiate a data row with UID and data
        RowClass = self.getInventoryRowClass()
        new_row = RowClass(inventory_object)

        self.logDebug(f'Adding a row for the {new_row.object.description} to the grid')
        self.add_widget(new_row)


    def fillUserData(self, app):
        '''Populate the data rows with user data during application startup'''
        self.logDebug(f'Filling the{self.category} DataGrid with objects')

        # Get access to the application instance
        if self.app == None:
            self.app = app

        # Get the containers or things to fill the data grid
        self.app.verifyObjectsLoaded()

        self.logDebug('Looping through the objects')
        if self.category == 'thing':
            objects = Thing.objs
        elif self.category == 'container':
            objects = Container.objs

        # Loop through the data and instantiate DataRows
        for key in objects:
            # Create the kv ContainerDataRow or ThingDataRow instance
            row_kv = self.getInventoryRowClass()(objects[key])

        self.updateWidgets()


    def getInventoryRowClass(self):
        ''' Return a reference to ContainerDataRow or ThingDataRow class'''
        if self.category == 'thing':
            return ThingDataRow
        elif self.category == 'container':
            return ContainerDataRow

    def getHeadingClass(self):
        ''' Return a reference to ContainerHeadingRow or ThingHeadingRow class'''
        if self.category == 'thing':
            return ThingHeadingRow
        elif self.category == 'container':
            return ContainerHeadingRow

    def deleteObject(self, UID):
        '''Delete a row from the GridLayout in the DataGrid. Also, remove the
           object data from app.inventory'''
        obj = InventoryObject.getByUID(UID)
        self.logDebug(f'Removing row {obj}..')
        # Delete the inventory object and its data
        obj.delete()

    def setDataGridObjectType(self, category):
        '''Set the category of object that this grid will be dealing with - ie "containers" or
           "things" - which will allow the instance to check which type of row/heading it will
           be instantiating
           Called in screens.py'''

        self.logDebug(f'Setting the DataGrid category to {category}')

        # Make sure the category is valid
        if category in DataGrid.categories:
            self.category = category

        # Create the heading widgets used to label the top of the data fields
        self.heading_row = self.getHeadingClass()()
        self.add_widget(self.heading_row)

    def updateWidgets(self):
        '''Update the visible Kivy objects on the DataGrid instance'''
        self.logInfo('Updating visible widgets..')
        for UID in InventoryObject.objs:
            self.logDebug(f'{InventoryObject.objs[UID]}')
            InventoryObject.objs[UID].updateWidget(self)

    def _assignColumnWidths(self):
        '''Loop thru each child widget that needs a fixed width and set its width.  This
           makes sure that each row has a uniform width.
        Comments:
            Not working.  Recieving 0 and 10 for x and y no matter the actual size
        Future maybe's:
            -Set the column width to the minimum needed width to fit the values
           '''
        self.logInfo('Assigning column widths')
        for row in self.dataRows:
            tex_width = self.dataRows[row].val_lo.width
            self.logDebug(f'Label size: {tex_width}')
            # tex_width = row.val_lo.texture_size
            # self.logDebug('kvLogic', f'Label size: {tex_width}')

    def _getMaxWidth(self):
        '''Loop thru each child widget's children and get the maximum width needed for the
        column'''
        self.logInfo(f'Did nothing...')
