'''  Manage inventory for Things and keep track of their value

    Improvements for future programs can include
        -Separating the logic layer from the presentation layer.  This program's
         logic is heavily intertwined with it's presentation which causes scalability
         issues.  Separating the presentation layer into a separate module would be a
         better solution.
        -Have the logic layer call for effects in the presentation layer OR
        -Have the logic layer gather necessary data and present it as needed
'''
from classes import Inventory, Box, Thing
from time import sleep
from resources.text_display import tablizeData
from resources import session
# import gui
import datetime
import json
import logging
import os
import sys
import traceback
import pymongo


class InventoryManagementApp():

    # Used to print out errors when self.draw() is called
    errors = []

    def __init__(self):
        # Initialize the logger
        self._initLog()

        # The screen that gets drawn and the objects the user has selected
        self.current_screen = self.sWelcome
        self.clearSubheading()
        self.selected_box = None
        self.selected_thing = None
        # The Inventory object reference created at runtime
        self.Inventory = None
        self.now = datetime.datetime.now()
        self.changes = 1

        # Get the width of the terminal for formatting
        if sys.platform == 'linux':
            xy = os.popen('stty size', 'r').read().split()
            self.cols = int(xy[1]) - 41
        else:
            self.cols = 40
        # Widths of data presentation
        self.field_widths = [4, self.cols, 6, 5, 7]

    def screen(self, screen):
        # If the user didn't input these characters
        if screen != 'help' and screen is not '?' and screen is not 'h':
            # self._reportError('screen input was not "help"')

            if screen == 'ov':  # Overview
                self.current_screen = self.sOverview
                self.draw()
            elif screen == 'mti':
                if self._hasBox() is True and self.selected_box.getInventory() == self.Inventory.boxes_not_in_inventory:
                    self.current_screen = self.sOverview
                    self.moveToInventory()
                else:
                    self._reportError('Please type "sb" to select a Box')
                self.draw()
            # Move thing
            elif screen == 'mt':
                if self._hasThing() is True:
                    self.current_screen = self.sOverview
                    self.move('thing')
                else:
                    self._reportError('Please type "st" to select a Thing')
                self.draw()
            elif screen == 'ct':
                if self._hasThing() is True and self._hasBox() is True:
                    self.current_screen = self.sViewBox
                    self.copy('thing')
            elif screen == 'save':
                self._save()
                self.draw()
            elif screen == 'load':
                self.current_screen = self.sLoad
                self.draw()
                self._loadData()
            elif screen == 'load backup':
                self.current_screen = self.sLoad
                self.draw()
                self._loadData(backup=True)
            # Save all objects and exit the python interpreter
            elif screen == 'exit':
                self._save()
                quit()

            # Update the screen to get rid of excess text output
            else:
                self.draw()

        elif screen == 'help' or screen is '?' or screen is 'h':  # Draw the help screen
            self.draw()
            self.sHelp()

    def backup(self):
        self.changes += 1
        if self.changes // 5 == 0:
            self._save(backup=True)

    def clearMemory(self):
        Inventory.resetClassAttributes()
        Box.resetClassAttributes()
        Thing.resetClassAttributes()

    def copy(self, tobject):
        '''Create a copy of a box or thing'''
        if tobject == 'thing':
            t = self.selected_thing
            new_thing = Thing(  t.getName(),
                                t.getValue(),
                                t.getWeight(),
                                t.getContainer(),
                                None,
                                t.getDateAcquired(copy=True))
            self.selected_thing = new_thing
            self.selected_box.addThing(self.selected_thing)

        self.draw()

    def createBox(self):
        self.subheading = ' -  -  -  Creating a new Box  -  -  -'
        self.draw()

        print('A new Box located at [___]')
        location = self.getInput(Box.defaults['location'])
        self.draw()

        print(f'A new Box located at -{location}-, with a weight of [___] lbs')
        weight = self.getInput(str(Box.defaults['weight']), return_num=True)
        self.draw()

        print(f'A new Box located at -{location}-, with a weight of -{weight}- lbs, and a value of $[___]')
        value = self.getInput(Box.defaults['value'], return_num=True)
        self.draw()

        # Create a new box object and add it to the inventory object
        self.selected_box = Box(location, weight, value, self.Inventory)
        self.Inventory.addNewBox(self.selected_box)
        self.clearSubheading()
        self.backup()

    def createThing(self):
        '''Create a new Thing object and assign it to the proper box if selected'''
        title = f' \n-  -  -  Creating a new Thing in Box {self.selected_box.getID()}  -  -  -'
        self.subheading = title
        self.draw()

        print(f'A new [___]..')
        name = self.getInput(Thing.defaults['name'])
        self.draw()

        print(f'A new -{name}-, with a value of $[___]...')
        value = self.getInput(Thing.defaults['value'], return_num=True)
        self.draw()

        print(f'A new Box located at -{name}-, with a value of -${value}-, and a weight of [___] lbs.')
        weight = self.getInput(Thing.defaults['weight'], return_num=True)
        self.draw()

        print(f'Enter the month and year you acquired this {name} in the format "4 2019"')
        month, year = self.getInput(f'{self.now.month} {self.now.year}', return_date=True)

        self.clearSubheading()
        self.draw()

        self.selected_thing = Thing(name, value, weight, self.selected_box, date_acquired=(month, year))
        self.selected_box.addThing(self.selected_thing)
        self.clearSubheading()
        self.backup()

    def deselect(self, tobject):
        if tobject is 'box':
            self.selected_box = None
            # self.selected_thing = None
        elif tobject is 'thing':
            self.selected_thing = None
            self._reportError(f'selected_thing = {self.selected_thing}')
        else:
            self._reportError(f'deselect( {tobject} )')
            self._reportError('Unexpected input')
        self.draw()

    def draw(self, pass_thru=None):
        '''
        Clear the screen and redraw the various headings
        pass_thru -> None or string of additonal text to print to the screen
        '''
        self.sClear()
        self.sHeading()
        self.sErrors()
        self.log.debug(self.current_screen)
        # If something was assigned to pass_thru pass it on to the next function
        if self.current_screen.__name__ != self.sFiles.__name__:
            self.current_screen()
        else:
            self.current_screen(pass_thru)
        if isinstance(self.subheading, type(None)) is True:
            pass
        elif isinstance(self.subheading, str) is True:
            print('\n' + self.subheading)
        else:
            with open(f + '.log', 'a') as traceback_f:
                traceback.print_stack(file=traceback_f)
            self.log.exception(f'self.subheading is not str or None.  Recieved: {subheading}')
            self._reportError(f'self.subheading is of type {type(self.subheading)}, not string')
            self.draw()

    def getCurrentOwner(self):
        if isinstance(self.Inventory, Inventory):
            return self.Inventory.getOwner()
        else:
            return None

    def getSavedNames(self, dir_str):
        '''
        Returns a list of files in the given directory relative to main.py
        dir_str -> directory name
        '''
        files = [f for f in os.listdir(dir_str) if os.path.isfile(os.path.join(dir_str, f))]
        self.log.debug(files)

        # Return file names without the extension ".inventory"
        for i in range(len(files)):
            try:
                files[i] = files[i][0:files[i].rfind('.')]
            except:
                files[i] = f'Error parsing file extension. Could not find the "." in {files[i]}'

        return files

    def getInput(self, tip_str=None, return_num=False, draw_pass_thru=None, return_date=False):
        '''
        Get input from the user and provide a tip or default option when pressing enter. If
        no tip_str is provided, ignore random enter presses.
        tip_str -> string denoting default user selection
        return_num -> Boolean denoting if input will only be accepted if it is a number
        draw_pass_thru -> None or text to pass thru to self.draw(), then self.current_screen()
        '''
        self.log.debug(f'tip_str: {tip_str}; return_num: {return_num}')

        user_input_flag = False
        while user_input_flag is False:
            user_input = input(self._getUserPromptString(tip_str))
            self.log.debug(f'Recieved user input of---{user_input}')

            # If the user presses enter without input...
            if user_input == '' and return_date is not True:
                # If there is a default...
                if tip_str is not None:
                    # Return the default
                    return tip_str
                # If there isn't a default restart the input process
                else:
                    self.draw(pass_thru=draw_pass_thru)

            # If the user enters something...
            else:
                # If a number is needed...
                if return_num is True:
                    # Try converting the string to a number
                    try:
                        user_input = float(user_input)
                        return user_input
                    # Log the insident and restart the input process
                    except ValueError:
                        self.log.debug(f'Failed to convert {user_input} to a number')
                        self.draw(pass_thru=draw_pass_thru)

                # If a date is needed...
                elif return_date is True:
                    if user_input is '':
                        tip_str = tip_str.split(' ')
                        tip_str[0] = int(tip_str[0])
                        tip_str[1] = int(tip_str[1])
                        return tip_str[0], tip_str[1]
                    # Try converting the string to a number
                    try:
                        user_input = user_input.split(' ')
                        if isinstance(user_input, list):
                            try:
                                user_input[0] = int(user_input[0])
                                user_input[1] = int(user_input[1])
                                return user_input[0], user_input[1]
                            except ValueError:
                                self.log.debug(f'Failed to convert {user_input} to a number for a date')
                                self.draw(pass_thru=draw_pass_thru)
                        else:
                            self.log.debug(f'Failed to split {user_input} into a month and year')
                            self.draw(pass_thru=draw_pass_thru)

                    # Log the insident and restart the input process
                    except ValueError:
                        self.log.debug(f'Failed to convert {user_input} to a date')
                        self.draw(pass_thru=draw_pass_thru)

                # If a number isn't needed return their input
                else:
                    return user_input

    def _getUserPromptString(self, tip_str=None):
        '''
        Return a custom user input prompt string
        tip_str -> string denoting default user selection
        '''
        self.log.debug(f'Recieved {tip_str} for tip_str')
        if tip_str is None:
            end_str = ' >>> '
        else:
            end_str = f' [{tip_str}]>>> '

        if isinstance(self.Inventory, Inventory) is True:
            start_str = f'{self.Inventory.owner}\'s Inventory'
        else:
            start_str = 'Inventory Management App'

        if isinstance(self.selected_box, Box) is True:
            box_str = f' | box {self.selected_box.getID()}'
        else:
            box_str = ''

        if isinstance(self.selected_thing, Thing) is True:
            thing_str = f' | {self.selected_thing.getName()}'
        else:
            thing_str = ''

        self.log.debug(f'Returning {start_str + end_str}')
        return start_str + box_str + thing_str + end_str

    def _hasInventory(self):
        '''Return True if an Inventory is assigned.  Return False if an Inventory is not assigned.'''
        if isinstance(self.Inventory, Inventory) is True:
            return True
        else:
            return False

    def _hasBox(self):
        '''Return True if a Box is selected.  Return False if a Box is not selected.'''
        if isinstance(self.selected_box, Box) is True:
            return True
        else:
            return False

    def _hasThing(self):
        '''Return True if a Thing is selected.  Return False if a Thing is not selected.'''
        if isinstance(self.selected_thing, Thing) is True:
            return True
        else:
            return False

    def clearSubheading(self):
        self.subheading = None

    def move(self, tobject):
        '''
        Move a Box or Thing to a diferent Box or location
        tobject -> 'thing' or 'box'
        '''
        if tobject is 'thing':
            if self._hasThing() is True:
                self.subheading =\
                    f'-Put the {self.selected_thing.getName()}-{self.selected_thing.getID()} into the Box with an ID of ___.'
                self.draw()
                ID = self.getInput(return_num=True)
                self.selected_thing.putInto(Box.getBox(ID))
        elif tobject is 'box':
            if self._hasBox() is True:
                self.subheading = f'-The Box\'s new location is ____.'
                self.draw()
                self.selected_box.setLocation(self.getInput(Box.getDefault('location')))
        else:
            self.log.warning(f'Recieved bad input for tobject.  Recieved {tobject}')

        self.clearSubheading()
        self.draw()
        self.backup()

    def moveToInventory(self):
        '''Move a box back into inventory'''
        # self.subheading = f'- - - Moving Box {self.selected_box.getID()} to a different inventory - - -'
        self.selected_box.moveToInventory(self.Inventory)
        self.draw()
        self.backup()

    def removeBox(self):
        if self._hasBox() is True:
            self.subheading = ' - - - Removing a Box - - - '
            self.draw()
            if self.Inventory.hasBox(self.selected_box.getID()) is True:
                print(' (r) Remove this box from inventory')
                print(' (X) Permanently delete the box and it\'s contents')
                response = self.getInput('cancel')
                if response is 'r':
                    self.Inventory.removeBox(self.selected_box.getID())
                elif response == 'X':
                    self.Inventory.deleteBox(self.selected_box.getID())
                    self.deselect('box')

            elif self.Inventory.hasBox(self.selected_box.getID()) is False:
                print(' (X) Permanently delete the box and it\'s contents')
                response = self.getInput('cancel')
                if response is 'X':
                    self.Inventory.deleteBox(self.selected_box.getID())
                    self.deselect('box')

        else:
            self._reportError('No box is selected! Use "sb" to select a box')

        self.clearSubheading()
        self.draw()
        self.backup()

    def removeThing(self):
        if self.selected_thing is not None:
            self.subheading = ' - - - Removing a Thing - - - '
            self.draw()
            # print(f'Would you like to destroy Thing {self.selected_thing.getID()} - {self.selected_thing.getName()} (y/n)?')
            # response = self.getInput('y')

            # if response == 'y':
            self.subheading = f' - - - Removing a(n) {self.selected_thing.getName()} with an ID of {self.selected_thing.getID()} - - - '
            if self.selected_thing.hasContainer() is True:
                self.draw()
                s = f'(r)     Remove the {self.selected_thing.getName()} from Box '
                s += f'{self.selected_thing.getContainer().getID()}'
                print(s)
                print(f'(X)     Permanently delete the {self.selected_thing.getName()}')
                print('(enter) Cancel')
                response = self.getInput()
                if response == 'r':
                    self.selected_box.removeThing(self.selected_thing)
                elif response == 'X':
                    self.selected_box.deleteThing(self.selected_thing)
                    self.deselect('thing')

            else:
                self.draw()
                print(f'        The {self.selected_thing.getName()} is not in a Box')
                print(f'(X)     Permanently delete the {self.selected_thing.getName()}')
                print(' ()  Cancel')
                response = self.getInput('Cancel')
                if response == 'X':
                    self.selected_box.deleteThing(self.selected_thing)
                    self.deselect('thing')

            self.clearSubheading()
        else:
            self._reportError('No Thing is selected')
            self.draw()

        self.backup()

    def run(self):
        '''Starts the application and handles the highest level loop'''

        self.log.debug('Starting the application')

        # Set the current screen to the welcome screen, create a subheading
        # and draw them to the terminal
        self.current_screen = self.sWelcome
        self.subheading = 'Please press enter'

        self.draw()
        self.getInput('Get Started')
        self.clearSubheading()

        self._loadData()

        self.screen('ov')

        running = True
        while running:

            userinput = self.getInput()
            self.screen(userinput)
            self.clearSubheading()

    def select(self, tobject):

        s = '   -   -   -   Selecting   -   -   -'

        if tobject == 'box':
            s += '\nBox ID selection: [__]'
            self.subheading = s
            self.draw()
            if Inventory.hasBoxes() is True:
                ID = self.getInput(return_num=True)
                try:
                    self.selected_box = self.Inventory.Boxes[ID]
                except KeyError:
                    try:
                        self.selected_box = self.Inventory.boxes_not_in_inventory[ID]
                    except KeyError:
                        self._reportError(f'No such Box ID: {ID}')
                        self.log.error(f'No boxes exist despite Invetory.hasBoxes() returning True!')
                        self.draw()

            else:
                self._reportError('No boxes exist!')
                self.draw()

        elif tobject == 'thing' and isinstance(self.selected_box, Box) is True:
            s += '\nThing ID selection: [__]'
            self.subheading = s
            self.draw()
            ID = self.getInput(return_num=True)
            try:
                self.selected_thing = self.selected_box.Things[ID]
            except KeyError:
                try:
                    self.selected_thing = Box.things_not_in_box[ID]
                except KeyError:
                    self._reportError(f'No Thing with the ID of {ID} was found')
                    self.log.debug(f'Failed to find Thing with ID of {ID}. Could not select')
                    self.draw()

        elif tobject == 'thing' and isinstance(self.selected_box, Box) is False:
            s += '\nThing ID selection: [__]'
            self.subheading = s
            self.draw()
            try:
                ID = int(self.getInput(return_num=True))
                self.selected_thing = Box.things_not_in_box[ID]
            except KeyError:
                self._reportError(f'No such Boxless Thing with ID: {ID}')
                self.draw()
        else:
            self._reportError(f'InventoryManagementApp.select( {tobject} )')
            self._reportError('Unexpected error')
            self._reportError(f'selected_box: {self.selected_box}')
            self._reportError(f'selected_thing: {self.selected_thing}')
            self.draw()

        self.clearSubheading()

    def sClear(self):
        def clear():
            return os.system('clear')
        clear()
        # self._reportError('\n\n--------screen pretend cleared here------------')

    def sErrors(self):
        if len(InventoryManagementApp.errors) > 0:
            # print('InventoryManagementApp.errors')
            for error in InventoryManagementApp.errors:
                print(error)
            self._clearErrors()
            print()

    def sFiles(self, file_names):
        '''
        Take file names without extensions for the user to select from
        file_names -> list of strings
        '''
        print('Please type one of the names below to load an inventory file.')
        print('Entering a new name will create a new inventory.')
        for name in file_names:
            print(name)
        print()

    def getHomelessThings(self):
        homeless_things_list = []
        homeless_things_list.append('Things not in a box:')
        if len(Box.things_not_in_box) > 0:
            hmless = Box.things_not_in_box  # pointer to dict of homeless things
            for key in hmless:
                homeless_things_list.append(f' --Thing {hmless[key].getID()} called {hmless[key].getName()}')
        else:
            homeless_things_list.append(' --Everything is boxed!')

        return homeless_things_list

    def sHomelessBoxes(self):
        s = 'Boxes not in inventory:'
        for key in Inventory.not_in_inventory.keys():
            s += f' ({Inventory.not_in_inventory[key].getID()}:{Inventory.not_in_inventory[key].getValue()})'
        print(s)
        print()

    def sHeading(self):
        # self.sClear()
        if self._hasBox() is True:
            box = self.selected_box.getID()
        else:
            box = None
        if self._hasThing() is True:
            thing = self.selected_thing.getName()
        else:
            thing = None
        if self._hasInventory() is True:
            owner = self.Inventory.getOwner()
        else:
            owner = None
        hyphen = '-' * self.cols
        print(f'- Inventory Management App {hyphen} (?, exit)')

    def sHelp(self):
        print('-        --      H e l p      --         -')
        print('   New Box: nb  |   New Thing: nt |   Move Box: mb')
        print('Delete Box: Db  |Delete Thing: Dt | Move Thing: mt')
        print('  Overview: ov  |    View Box: vb |   New Inv.: NI')
        print('Select Box: sb  |        help: h  | Copy Thing: ct')
        print('                |Select Thing: st |')
        print()

    def sWelcome(self):
        print('View and manage your personal storage for easier finding and doing.')
        print()

    def sLoad(self):
        if self.Inventory is not None:
            print(f'All changes will be saved to {self.Inventory.getOwner()}\'s Inventory.')
        print('Type the name of a user inventory found below or type a new name')
        print()

    def sOverview(self):
        '''Display basic information about the user's inventory'''
        print(f'    Overview')
        total_width = sum(self.field_widths)
        print(f'Total value: ~${self.Inventory.getValue()}')
        print(f'Total weight: ~{self.Inventory.getWeight()} lbs')
        print()
        self.sInventory()

    def sInventory(self):
        '''Display boxes in the inventory'''
        if len(self.Inventory.Boxes.keys()) == 0:
            print('   -You have no Boxes in your Inventory!-')
        else:
            headings = ['ID', 'Location', 'Weight', 'Value', 'Acquired']
            bxs = self.Inventory.Boxes
            data_lists = []

            for key in bxs.keys():
                data_list = []
                data_list.append(bxs[key].getID())
                data_list.append(bxs[key].getLocation())
                data_list.append(int(bxs[key].getWeight()))
                data_list.append('$' + str(int(bxs[key].getValue())))
                data_list.append(bxs[key].getDateAcquired())
                data_lists.append(data_list)

            if self._hasBox() is True:
                tablizeData(headings, self.field_widths, data_lists, self.selected_box.getID(), id_row=0)
            else:
                tablizeData(headings, self.field_widths, data_lists)

    def sViewBox(self):
        if len(self.Inventory.Boxes.keys()) == 0:
            print('   -You have no Boxes in your Inventory!-')
        else:
            headings = ['ID', 'Name', 'Weight', 'Value', "Acquired"]
            thngs = self.selected_box.Things
            data_lists = []

            for key in thngs.keys():
                data_list = []
                data_list.append(thngs[key].getID())
                data_list.append(thngs[key].getName())
                data_list.append(int(thngs[key].getWeight()))
                data_list.append('$' + str(int(thngs[key].getValue())))
                data_list.append(thngs[key].getDateAcquired())
                data_lists.append(data_list)

            if self._hasThing() is True:
                tablizeData(headings, self.field_widths, data_lists, self.selected_thing.getID(), id_row=0)
            else:
                tablizeData(headings, self.field_widths, data_lists)

    def sSaveConfirmation(self):
        self.subheading = '- - - - - Saving {self.Inventory.getOwner()}\'s data - - - - -'
        files = self.getSavedNames('saves')
        for f in files:
            print(f)
        print()

    def _constructObjects(self, data, name):
        '''
        Reconstruct save data into usable objects
        data -> dictionary
        name -> string
        '''
        self.Inventory = Inventory(owner=name)

        # For each saved box info dictionary...
        for B in data['Box']['Boxes']:
            # Create a new box through the Inventory.newBox method so it can capture needed information
            self.Inventory.loadSavedBox(B)
            # self.log.critical(f"location: {B['location']}, box_weight: {B['box weight']}")

            erase = []
            # For each saved thing info dictionary...
            for T in data['Thing']['Things']:
                # If this thing's ID matches an ID belonging to a box...
                if T['ID'] in B['thing IDs']:
                    name = T['name']
                    try:
                        value = float(T['value'])
                    except ValueError:
                        self.log.critical(
                            f''''Could not convert T['value'] to float! Assigning without conversion!''')
                        self.log.critical(f'''Recieved type {type(T['value'])} with value {T['value']}''')
                        value = T['value']
                    try:
                        weight = float(T['weight'])
                    except ValueError:
                        self.log.critical(
                            f''''Could not convert T['weight'] to float! Assigning without conversion!''')
                        self.log.critical(f'''Recieved type {type(T['weight'])} with value {T['weight']}''')
                        weight = T['weight']
                    try:
                        container_ID = int(T['container ID'])
                    except ValueError:
                        if isinstance(T['container ID]'], int):
                            self.log.warning(f'''Expected string for T['container ID']''')
                            container_ID = T['container ID]']
                        else:
                            self.log.critical(
                                f''''Could not convert T['container ID'] to int! Assigning without conversion!''')
                            self.log.critical(f'''Recieved type {type(T['container ID'])} with value {T['container ID']}''')
                            container_ID = T['container ID]']
                    try:
                        date_acquired = (T['date acquired'].split('/')[0], T['date acquired'].split('/')[1])
                    except ValueError:
                        self.log.error(
                            f''''Could not parse T['date acquired']! Assigning 0 values!''')
                        self.log.error(f'''Recieved type {type(T['container ID'])} with value {T['container ID']}''')
                        date_acquired = (0, 0)
                    try:
                        ID = int(T['ID'])
                    except ValueError:
                        self.log.critical(
                            f''''Could not parse T['date acquired']! Assigning 0 values!''')
                        self.log.critical(f'''Recieved type {type(T['container ID'])} with value {T['container ID']}''')
                        ID = T['ID']

                    self.log.debug(
                        f'Name: {name}, value: {value}, weight: {weight}, container_ID: {container_ID}, ID: {ID}, date_acquired: {date_acquired}')

                    self.Inventory.Boxes[B['ID']].newThing(
                        name,
                        value,
                        weight,
                        self.Inventory.Boxes[container_ID],
                        ID,
                        date_acquired
                    )
                erase.append(T)

            Box.IDer = data['Box']['IDer']
            Thing.IDer = data['Thing']['IDer']

            # # Erase Thing data that was already used
            # # Used to be sure we saved everything at the end of the function
            # for E in erase:
            #     if E in data['Thing']['Things']:
            #         data['Thing']['Things'].remove(E)
            # self.log.debug(data['Thing']['Things'])

    def _initLog(self):
        '''
        Debug:  Detailed information for debugging purposes
        Info:  Confirmation that things are working as expected
        Warning:  Indication that something unexpected happened or there is a potential problem in the future: Disk space low
        Error:  Due to a serious problem, the software failed to complete a function
        Critical:  A problem likely to cause the program to stop working
        '''
        now = datetime.datetime.now()
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.WARNING)
        f = f'logs/main.{now.day}.{now.month}.{now.year}'
        file_handler = logging.FileHandler(f + '.log')
        file_handler.setFormatter(
            logging.Formatter(
                f'{now.hour}:{now.minute}>%(levelname)s:%(name)s:%(funcName)s:%(lineno)s >>> %(message)s'
            )
        )
        self.log.addHandler(file_handler)

    def _reportError(self, info):
        '''
        Add the input into the errors list
        info -> string or list of strings
        '''
        if isinstance(info, str):
            InventoryManagementApp.errors.append(info)
        elif isinstance(info, list):
            for info_str in info:
                InventoryManagementApp.errors.append(info_str)

    def _save(self, local=False, backup=False):
        if local is True:
            inv_box_dict = self.Inventory.Boxes
            homeless_boxes = Inventory.boxes_not_in_inventory
            homeless_things = Box.things_not_in_box

            data = {"Inventory": {
                'Inventories': self.Inventory.getSaveData()
            },
                "Box": {
                'Boxes': [inv_box_dict[box_ID].getSaveData() for box_ID in self.Inventory.Boxes.keys()],
                'Boxes not in Inventory': [homeless_boxes[box_ID].getSaveData() for box_ID in homeless_boxes.keys()],
                'IDer': Box.IDer
            },
                "Thing": {
                'Things': [inv_box_dict[box_ID].Things[thing_ID].getSaveData()
                           for box_ID in inv_box_dict.keys() for thing_ID in inv_box_dict[box_ID].Things.keys()],
                'Things not in Box': [homeless_things[thing_ID].getSaveData() for thing_ID in homeless_things.keys()],
                'IDer': Thing.IDer
            }
            }

            if backup is True:
                file_str = f'backups/{self.Inventory.getOwner()}.inventory_backup'
                with open(file_str, 'w') as outfile:
                    json.dump(data, outfile, indent=4)

            else:
                with open(f'saves/{self.Inventory.getOwner()}.inventory', 'w') as outfile:
                    json.dump(data, outfile, indent=4)

        elif local is False and backup is False:
            self.database

    def _login(self):
        '''Log the user in using a MongoClient with user-provided credentials from the gui module'''
        from getpass import getpass
        logged_in = False
        while not logged_in:
            username = input('Username: ')
            # Create an inactive connection handler that waits to be used
            # Defaults to port 27017, otherwise use: f'mongodb://Craig:secretpwd@10.0.0.8:{PORT}/testdb1'
            client_connection = pymongo.MongoClient(
                f'mongodb://{username}:{getpass()}@10.0.0.8/{username.lower()}_inventory'
            )

            try:
                # Test authentication by creating and then deleting a document on the database
                # Clear the client_connection variable to reduce the risk of comprimised login info
                self.database = client_connection[f'{username.lower()}_inventory']
                client_connection = None
                test_collection = self.database.test
                inserted = test_collection.insert_one({'test': True})
                test_collection.delete_one({'_id': inserted.inserted_id})
                print('success!')
                logged_in = True
            except pymongo.errors.OperationFailure:
                client_connection = None
                print('Username and/or password is incorrect!')
                # If the user doesn't have access to the database or the user doesn't exist
                self._reportError('Username and/or password is incorrect!')
                self.log.error('Username and/or password is incorrect!')
            self.draw()

        self.draw()

    def _loadData(self, local=False, backup=False):
        '''
        Interactive load screen for the user.  Show the user save files and ask them to type a name in.
        Handle spelling errors and ask the user if they would like to save the current inventory.
        '''

        self.log.critical(f'Owner: {self.getCurrentOwner()}')

        if backup is False:
            # Get the file names and present them to the user with draw()
            folder = 'saves'
            extension = 'inventory'
            file_owner_strings = self.getSavedNames(folder)

        elif backup is True:
            folder = 'backups'
            extension = 'inventory_backup'
            file_owner_strings = self.getSavedNames(folder)

        self.current_screen = self.sFiles
        self.draw(pass_thru=file_owner_strings)

        looping = True
        while looping is True:
            if len(file_owner_strings) > 0:
                # Prompt the user for input using the given argument as the default for pressing "enter"
                input_name = self.getInput(file_owner_strings[0], draw_pass_thru=file_owner_strings)
            else:
                input_name = self.getInput(draw_pass_thru=file_owner_strings)

            # See if the user input an existing user name
            if input_name in file_owner_strings:
                # Try block to handle FileNotFoundError.  Will catch misspelled files, but not other errors.
                try:
                    self.__init__()
                    self.clearMemory()
                    # Load the file and store it in the data variable.  Log the data
                    with open(f'{folder}/{input_name}.{extension}', 'r') as infile:
                        data = json.load(infile)
                        self.log.critical(data)

                    # # If an inventory is selected prompt the user to see if they want to save the inventory
                    # if self.Inventory is not None:
                    #     self.subheading = f'Would you like to save {self.getCurrentOwner()}\'s inventory?'
                    #     self.draw(pass_thru=file_owner_strings)
                    #     input_save = self.getInput('y')

                    #     # Save the data if the user presses enter or 'y'
                    #     if input_save == 'y':
                    #         self._save()

                    self._constructObjects(data, input_name)
                    looping = False

                # If the file was not found, log the information
                except FileNotFoundError:
                    self.log.debug(f'No file found with the name "{input_name}.{extension}"')

            elif input_name is not '':
                self.subheading = f'Would you like to create a new inventory for {input_name}?'
                self.draw(pass_thru=file_owner_strings)
                input_answer = self.getInput('y')
                if input_answer is 'y':
                    self.__init__()
                    self.clearMemory()
                    self.Inventory = Inventory(input_name)
                    looping = False
                else:
                    # Retry the loop
                    pass

            # Clear the screen
            self.draw(pass_thru=file_owner_strings)

        # Set the screen to overview
        self.clearSubheading()
        self.draw()

    def _clearErrors(self):
        InventoryManagementApp.errors = []


if __name__ == '__main__':
    App = InventoryManagementApp()
    App._login()
