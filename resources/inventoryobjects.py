from resources.utilities import LogMethods
from kivy.logger import Logger
from json import dumps

class InventoryObject():
    '''Parent class for inventory objects with base methods and class methods
       that make managing the inventory easier'''
    ID_counter = 0         # Unique ID counter for each of the user's objects
    objs = {}               # All InventoryObject and inherited instances
    selected = None         # The selected InventoryObject instance (or inherited)
    changes_made = False    # Flag to determine whether a save is needed
    def __init__(
            self,
            ID='0',
            description='A void InventoryObject instance',
            usd_value=0,
            weight=0,
            tags='',
            things=None,
            container=None     ):
        '''Create an instance of Inventory object and assign its ID, description,
           USD value, weight, and tags. Add it to the InventoryObject.objs dictionary
           Takes input:
           ID - int as a string
           description - string
           usd_value - int as string
           weight - int as string
           tags - single-word or multi-word (separated by _) tags separated by a space
           things - None; dummy kwarg to prevent errors from kwarg unpacking from file load
           container -  None; dummy kwarg to prevent errors kwarg unpacking from file load'''
        self.ID = ID
        self.description = description
        self.usd_value = usd_value
        self.weight = weight
        self.tags = []
        self.widget = None
        self.grid = None
        self.addTags(tags)
        InventoryObject.objs[self.ID] = self

    def addTags(self, tags):
        '''Take a string or list of tags and adds them to self.tags as a list'''
        # Combine the list of tags
        if isinstance(tags, list):
            self.tags += tags
            self.changes_made = True
        # Turn the string into a list of tags and combine it with tags
        elif isinstance(tags, str) and tags != '':
            # Remove surrounding blank characters and split the tags up by spaces
            tags = tags.strip()
            tags = tags.split(' ')
            # Replace underscores with spaces
            for n in range(len(tags)):
                tags[n] = tags[n].replace('_', ' ')
            self.tags += tags
            self.changes_made = True

    def changeMade(self):
        '''Set the changes_made flag for saving data in the future'''
        self.changes_made = True

    def delete(self):
        '''Remove the widget and delete the instance from the InventoryObject.objs dict'''
        self.widget.object = None
        self.grid.remove_widget(self.widget)
        del InventoryObject.objs[self.ID]

    def drawWidget(self):
        '''Draw the widget if it isn't already'''
        if self.widget not in self.grid.children:
            self.logDebug(f'Drawing widget {self.widget}')
            self.grid.add_widget(self.widget)

    def hasParent(self):
        '''Return True if the widget is drawn, False otherwise'''
        if self.widget != None:
            if self.widget.parent != None:
                return True
        return False

    def hasWidget(self):
        '''Return True if the object has a widget, False otherwise'''
        if self.widget != None:
            return True
        else:
            return False

    def removeTags(self, tags):
        '''Take a string of user-input tags and remove them from searchable tags'''
        if tags != '':
            # Remove surrounding blank characters and split the tags up by spaces
            tags = tags.strip()
            tags = tags.split(' ')
            # Replace underscores with spaces
            for n in range(len(tags)):
                tags[n] = tags[n].replace('_', ' ')

            for tag in tags:
                if tag in self.tags:
                    self.tags.remove(tag)

            self.changes_made = True

    def saveNeeded(self):
        '''Return True if a save is needed, False otherwise'''
        if self.changes_made == True:
            return True
        else:
            return False

    def undrawWidget(self):
        '''Undraw the widget if it is drawn'''
        if self.widget in self.grid.children:
            self.logDebug(f'Undrawing widget {self.widget}')
            self.grid.remove_widget(self.widget)

    def wasChanged(self):
        if InventoryObject.changes_made == True:
            return True
        else:
            return False

    @classmethod
    def getByID(cls, ID):
        '''Return an object with the give ID (str)'''
        if ID in cls.objs.keys():
            return cls.objs[ID]
        else:
            return None

    @classmethod
    def getSaveData(cls):
        '''Return a dictionary of json serializable data for saving to a file'''
        data = {
            'thing': {},
            'container': {}
        }
        for ID, obj in cls.objs:
            if isinstance(obj, Thing):
                d = data['thing']
                d[ID] = {}
                d[ID]['container'] = obj.container.ID

            elif isinstance(obj, Container):
                d = data['container']
                d[ID] = {}
                d[ID]['things'] = list(obj.things)

            else:
                Logger.critical(
                    ':There is an unidentified object type in InventoryObject.objs'
                )

            d[ID]['description'] = obj.description
            d[ID]['usd_value'] = obj.usd_value
            d[ID]['weight'] = obj.weight
            d[ID]['tags'] = obj.tags

        Logger.debug(dumps(data))

        return data

    @classmethod
    def getNewID(cls):
        '''Increment cls.ID_counter and return it as a ID'''
        invalid = True
        while invalid:
            cls.ID_counter += 1  # Increment the ID counter
            Logger.debug(f':app.ID_counter incremented to {cls.ID_counter}')
            if cls.ID_counter not in cls.objs:
                Logger.debug(f':Returning app.ID_counter {cls.ID_counter}')
                return cls.ID_counter

    @classmethod
    def updateWidgets(cls, grid):
        '''Draw and undraw widgets based on the currently viewed screen'''
        Logger.debug(f': Updating widgets for {cls.selected}')
        for ID in cls.objs:
            if ID not in cls.objs:
                raise KeyError(f'Key {ID} not found in cls.objs')
            Logger.debug(f': Updating: {cls.objs[ID]}')
            cls.objs[ID].updateWidget(grid)

    @classmethod
    def checkLoad(cls):
        for ID in cls.objs:
            if isinstance(cls.objs[ID], Thing):
                Logger.debug(f': {cls.objs[ID].description} container: {cls.objs[ID].container}')
            else:
                Logger.debug(f': {cls.objs[ID].description} things: {cls.objs[ID].things}')





class Thing(InventoryObject, LogMethods):
    '''Child class that handles things not meant to be containers'''
    objs = {}   # Keeps the Thing instances as ID: object pairs
    def __init__(self, kwargs):
        '''Create a new Thing and call the parent __init__ method.  Initialize the log.
           Add the Thing to the Thing.objs dict.'''
        super(Thing, self).__init__(**kwargs)
        self.__initLog__(file_str='inventoryobjects.py', class_str='Thing')
        self.logDebug(f'Thing.__init__(kwargs): {dumps(kwargs, indent=4)}')

        # Handle taking this from a loaded file with a saved container..
        try:
            self.container = kwargs['container']
        # ..or as a newly created instance without one
        except KeyError:
            self.container = self.selected

        Thing.objs[self.ID] = self
        self.category = 'thing'

    def __repr__(self):
        s = f'<Thing object {self.description} with ID {self.ID}>'
        return s

    def delete(self):
        '''Delete references to the instance and call the parent's delete method'''
        self.changeMade()
        del Thing.objs[self.ID]
        super(Thing, self).delete()

    def getContainer(self):
        '''Return the Thing's Container object'''
        return InventoryObject.getByID(self.container)

    def inContainer(self):
        '''Determine if this Thing is assigned to a Container'''
        if self.container != None:
            return True
        else:
            return False

    def isInside(self):
        '''Return the Container for this Thing'''
        return self.getByID(self.container)

    def updateWidget(self, grid=None):
        '''Make sure the widget has a DataGrid assigned and the widget category matches the
           grid's. Add the grid if necessary.  Check if the widget needs to be drawn and
           draw if necessary.'''

        # If the Thing has no DataGrid assigned and the category matches, assign it
        self.logDebug(f'{self.description} is checking for a grid')

        if self.grid == None and grid != None and self.category == grid.category:
            self.logDebug(f'Grid not found. Added grid to {self.description}')
            self.grid = grid

        # If the Thing instance is in the selected Container instance, draw the widget
        if self.selected != None and self.selected.contains(self) == True:
            self.logDebug(f'Drawing widget for {self}')
            self.drawWidget()
        # If the Thing is not in the selected Container, undraw the widget
        elif self.selected != None and self.selected.contains(self) == False:
            self.logDebug(f'Undrawing widget for {self}')
            self.undrawWidget()




class Container(InventoryObject, LogMethods):
    '''Child class that handles special container methods'''
    objs = {}       # Contains all Container instances
    def __init__(self, kwargs):
        '''Create a container instance, call the parent class __init__ and assign its
           attributes'''

        # Handle a loaded file
        try:
            self.things = kwargs['things']
        # Handle a newly created Container
        except KeyError:
            self.things = []

        # Call the parent __init__ method to assign attributes and init the log
        super(Container, self).__init__(**kwargs)
        self.__initLog__(file_str='inventoryobjects.py', class_str='Container')

        # Add the instance to the Container.objs dict and set the category of the object
        Container.objs[self.ID] = self
        self.category = 'container'

    def __repr__(self):
        s = f'<Container object {self.description} with ID {self.ID} '
        s += f'and {len(self.things)} Thing(s)'
        return s + '>'

    def addThing(self, ID):
        '''Add a thing to the container. Turn self.things into a dict if it hasn't been,
           add the Thing to self.things and flag a change'''
        self.logDebug(f'Adding Thing {ID} to Container {self.ID}')
        InventoryObject.getByID(ID).container = self.ID
        self.things.append(ID)
        self.changeMade()

    def delete(self):
        '''Flag a change, fix self.things if necessary, delete any contents and call the
           parent delete method'''
        self.changeMade()

        # Check for and delete any contents
        if self.hasContents():
            for ID in self.things:
                InventoryObject.getByID(ID).delete()

        # Delete any other references to the Container
        del Container.objs[self.ID]
        super(Container, self).delete()

    def hasContents(self):
        '''Check for contents and return True or False'''
        if len(self.things) > 0:
            return True
        else:
            return False

    def contains(self, thing):
        '''Check if a specific Thing or ID is in the Container and return True or False'''
        if isinstance(thing, int):
            if str(thing) in self.things:
                self.logDebug(f'{self.description} contains {thing} in {self.things}')
                return True
            else:
                self.logDebug(f'{self.description} doesn\'t contain {thing} in {self.things}')
                return False
        elif isinstance(thing, (Thing, Container)):
            if str(thing.ID) in self.things:
                return True
            else:
                return False
        else:
            raise TypeError(f'Type {type(thing)} not valid. Must be int, Thing, or Container')

    def removeThing(self, thing):
        '''Remove the provided Thing object if it is inside the Container'''
        if isinstance(thing, int):
            if thing in self.things:
                self.changeMade()
                InventoryObject.getByID(thing).updateContainer(None)
                del self.things[thing]
        elif isinstance(thing, (Thing, Container)):
            if thing.ID in self.things:
                self.changeMade()
                thing.updateContainer(None)
                del self.things[thing.ID]
        else:
            raise TypeError(f'Type {type(thing)} not valid. Must be int, Thing, or Container')

        if thing.ID in self.things:
            self.changeMade()
            thing.updateContainer(None)
            del self.things[thing.ID]

    def updateWidget(self, grid=None):
        '''Make sure the widget has a DataGrid assigned and the widget category matches the
           grid's. Add the grid if necessary.  Check if the widget needs to be drawn and
           draw if necessary.'''

        self.logDebug(f'{self.description} is checking for a grid')
        if self.grid == None and grid != None and self.category == grid.category:
            self.logDebug(f'No grid found. Added to Container {self.ID}')
            self.grid = grid

        if self.category == grid.category:
            self.drawWidget()

