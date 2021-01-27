from json import dumps

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from resources.utilities import LogMethods
from resources.inventory import Inventory
from graphics.row2 import HeadingRow, DataRow


class DataGrid(GridLayout, LogMethods):

    def __init__(self, **kwargs):
        '''Creates the widgets in a user-defined manner'''
        # Init the parent, ScrollView
        super(DataGrid, self).__init__(**kwargs)
        self.__initLog__(file_str='datagrid.py', class_str='DataGrid')

        self.app = None
        self.clicked = None

    def __repr__(self):
        s = f'<DataGrid object with parent: >'
        return s

    def on_touch_down(self, touch):
        '''This allows me to get click/touch coordinates from the user. Without calling
           the super method, buttons and other UI elements don't respond to clicks.'''

        self.logDebug(f'\nClick-{touch.pos}')
        super().on_touch_down(touch)
        Inventory.setBounds(self, touch)

        row_clicked = False
        # Check which widget was clicked
        # For each widget in self.children
        for widget in self.children:

            # Check if it is a DataRow instance rather than a heading row
            if isinstance(widget, DataRow):
                was_clicked = widget.wasClicked(touch)

                if was_clicked == True:
                    row_clicked = True
                    self.app.selection(widget.inventory)

                    # Check for a double-click
                    if touch.is_double_tap:
                        self.logDebug(f'Double-click detected')

                        # If inventory with contents is double-clicked, change screen
                        if isinstance(widget, DataRow) and widget.inventory.hasContents() == True:
                            self.app.changeScreen(widget.inventory.ID)
                            self.app.selection(None)
                        # If a thing is selected, pass
                        elif isinstance(widget, DataRow) and widget.inventory.hasContents() == False:
                            pass
                        else:   # Empty space clicked.  Deselect
                            self.app.selection(None)

        if row_clicked == False:
            self.app.selection(None)

        self.app.sm.current_screen.toolbar.presentOptions()

    def addDataRow(self, inventory):
        '''Add a row of fields to the GridLayout with the given data
           data is a dict of user input'''

        # Add the datagrid to the widget
        if inventory.parent_widget == None:
            inventory.parent_widget = self

        # Instantiate a data row with ID and data
        new_row = DataRow(inventory)

        inventory.widget = new_row

        self.logDebug(f'Adding a row for the {new_row.object.description} to the grid')
        self.add_widget(new_row)

    def deleteObject(self):
        '''Delete an object and its row from the GridLayout in the DataGrid'''
        # Delete the inventory object and its data
        selection = self.app.selection.get().getObj()
        if selection.hasContents() == True:
            self.logDebug(f'{selection} has contents. Warning user.')
            self.app.createPopup(warn=True)
        else:
            selection.delete()

    def fillUserData(self, app):
        '''Populate the data rows with user data during application startup'''
        self.logDebug(f'Filling the DataGrid with objects')

        # # Get access to the application instance
        # if self.app == None:
        #     self.app = app

        Inventory.updateWidgets(self)
