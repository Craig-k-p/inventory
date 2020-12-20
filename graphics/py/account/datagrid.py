from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.graphics.instructions import InstructionGroup
from kivy.properties import ObjectProperty

from resources.utilities import LogMethods
from resources.inventoryobjects import Thing, Container, InventoryObject
from graphics.py.account.row import ContainerHeadingRow, ContainerDataRow
from graphics.py.account.row import ThingHeadingRow, ThingDataRow, DataRow
from json import dumps


class DataGrid(GridLayout, LogMethods):

    categories = ('container', 'thing')

    # # Store the ContainerDataRow instances here
    # dataRows = {'containers': {}, 'things': {}}

    def __init__(self, **kwargs):
        '''Creates the widgets in a user-defined manner'''
        # Init the parent, ScrollView
        super().__init__(**kwargs)
        self.__initLog__(file_str='kv_DG.py', class_str='DataGrid')

        self.logInfo('Creating DataGrid instance')

        self.app = None

        self.heading_color = None
        self.row_1_color = None
        self.row_2_color = None

        self.category = None
        self.clicked = None

    def __repr__(self):
        s = f'<<{self.category} DataGrid>>'
        return s

    def on_touch_down(self, touch):
        '''This allows me to get click/touch coordinates from the user. Without calling
           the super method, buttons and other UI elements don't respond to clicks.'''

        self.logDebug(f'\nClick-{touch.pos}')
        super().on_touch_down(touch)
        InventoryObject.setBounds(self, touch)

        row_clicked = False
        # Check which widget was clicked
        # For each widget in self.children
        for widget in self.children:

            # Check if it is a DataRow instance rather than a heading row
            if isinstance(widget, (ContainerDataRow, ThingDataRow)):
                was_clicked = widget.wasClicked(touch)

                if was_clicked == True:
                    row_clicked = True
                    self.app.Selection(widget.object)

                    # Check for a double-click
                    if touch.is_double_tap:
                        self.logDebug(f'Double-click detected')

                        # If container is double-clicked, change screen
                        if isinstance(widget, ContainerDataRow):
                            self.app.buttonPress('changeScreen', 'container', 'left')
                            self.app.Selection(None)
                        # If a thing is selected, pass
                        elif isinstance(self.clicked, ThingDataRow):
                            pass
                        else:   # Empty space clicked.  Deselect
                            self.app.Selection(None)

        if row_clicked == False:
            self.app.Selection(None)

        self.app.sm.current_screen.toolbar.presentOptions()

    def addDataRow(self, inventory_object):
        '''Add a row of fields to the GridLayout with the given data
           data is a dict of user input'''


        # Allow easy access to the app instance
        if self.app == None:
            self.app = self.parent.parent.parent.parent.app

        # Add the datagrid to the widget
        if inventory_object.data_grid == None and self.category == inventory_object.category:
            inventory_object.data_grid = self

        # Instantiate a data row with ID and data
        RowClass = self.getInventoryRowClass()
        new_row = RowClass(inventory_object)

        inventory_object.widget = new_row

        self.logDebug(f'Adding a row for the {new_row.object.description} to the grid')
        self.add_widget(new_row)

    def deleteObject(self):
        '''Delete an object and its row from the GridLayout in the DataGrid'''
        # Delete the inventory object and its data
        self.app.Selection.get().getObj().delete()
        InventoryObject.changeMade()

    def fillUserData(self, app):
        '''Populate the data rows with user data during application startup'''
        self.logDebug(f'Filling the{self.category} DataGrid with objects')

        # Get access to the application instance
        if self.app == None:
            self.app = app

        # Get the containers or things to fill the data grid
        self.app.loadData()
        InventoryObject.updateWidgets(self)

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

    def setDataGridObjectType(self, category):
        '''Set the category of object that this grid will be dealing with - ie "containers"
           or "things" - which will allow the instance to check which type of row/heading
           it will be instantiating
           Called in screens.py'''

        self.logDebug(f'Setting the DataGrid category to {category}')

        # Make sure the category is valid
        if category in DataGrid.categories:
            self.category = category

        # Create the heading widgets used to label the top of the data fields
        self.heading_row = self.getHeadingClass()()
        self.add_widget(self.heading_row)

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
