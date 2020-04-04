from resources.utilities import LogMethods
from kivy.logger import Logger
from json import dumps

class InventoryObject():
    '''Parent class for inventory objects with base methods and class methods
       that make managing the inventory easier'''
    debug = True
    uid_counter = 0         # Unique ID counter for each of the user's objects
    objs = {}               # All InventoryObject and inherited instances
    selected = None         # The selected InventoryObject instance (or inherited)
    changes_made = False    # Flag to determine whether a save is needed
    def __init__(
            self,
            UID='0',
            description='A void InventoryObject instance',
            usd_value=0,
            weight=0,
            tags='',
            things=None,
            container=None     ):
    '''Create an instance of Inventory object and assign its UID, description,
       USD value, weight, and tags. Add it to the InventoryObject.objs dictionary
       Takes input:
       UID - int as a string
       description - string
       usd_value - int as string
       weight - int as string
       tags - single-word or multi-word (separated by _) tags separated by a space
       things - None; dummy kwarg to prevent errors from kwarg unpacking from file load
       container -  None; dummy kwarg to prevent errors kwarg unpacking from file load
       '''
        self.UID = UID
        self.description = description
        self.usd_value = usd_value
        self.weight = weight
        self.tags = []
        self.widget = None
        self.grid = None
        self.addTags(tags)
        InventoryObject.objs[self.UID] = self

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

    def delete(self):
        '''Remove the widget and delete the instance from the InventoryObject.objs dict'''
        self.widget.object = None
        self.grid.remove_widget(self.widget)
        del InventoryObject.objs[self.UID]

    def drawWidget(self):
        '''Draw the widget if it isn't already'''
        if self.widget not in self.grid.children:
            self.logDebug(f'Adding widget {self.widget}')
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

    def undrawWidget(self):
        '''Undraw the widget if it is drawn'''
        if self.widget in self.grid.children:
            self.logDebug(f'Removing widget {self.widget}')
            self.grid.remove_widget(self.widget)

    def saveNeeded(self):
        '''Return True if a save is needed, False otherwise'''
        if self.changes_made == True:
            return True
        elif self.changes_made == False:
            return False
        else:
            raise Exception(f'self.changes_made was unexpected: {self.changes_made}')

    @classmethod
    def getByUID(cls, UID):
        '''Return an object with the give UID (str)'''
        if UID in cls.objs.keys():
            return cls.objs[UID]
        else:
            return None

    @classmethod
    def getSaveData(cls):
        '''Return a dictionary of json serializable data for saving to a file'''
        data = {
            'thing': {},
            'container': {}
        }
        for o in cls.objs:
            obj = cls.objs[o]

            if isinstance(obj, Thing):
                d = data['thing']
                d[o] = {}
                d[o]['container'] = obj.container.UID

            elif isinstance(obj, Container):
                d = data['container']
                d[o] = {}
                d[o]['things'] = list(obj.things)

            else:
                Logger.critical(
                    ':There is an unidentified object type in InventoryObject.objs'
                )

            d[o]['description'] = obj.description
            d[o]['usd_value'] = obj.usd_value
            d[o]['weight'] = obj.weight
            d[o]['tags'] = obj.tags

        Logger.debug(dumps(data))

        return data

    @classmethod
    def getNewUID(cls):
        '''Increment cls.uid_counter and return it as a UID'''
        invalid = True
        while invalid:
            cls.uid_counter += 1  # Increment the ID counter
            Logger.debug(f':app.uid_counter incremented to {cls.uid_counter}')
            if str(cls.uid_counter) not in cls.objs:
                Logger.debug(f':Returning app.uid_counter {cls.uid_counter}')
                return str(cls.uid_counter)

    @classmethod
    def updateWidgets(cls, grid):
        '''Draw and undraw widgets based on the currently viewed screen'''
        Logger.debug(f': Updating widgets for {cls.selected}')
        for UID in cls.objs:
            Logger.debug(f':Updating: {cls.objs[UID]}')
            cls.objs[UID].updateWidget(grid)





class Thing(InventoryObject, LogMethods):
    '''Child class that handles things not meant to be containers'''
    objs = {}   # Keeps the Thing instances as UID: object pairs
    def __init__(self, kwargs):
        '''Create a new Thing and call the parent __init__ method.  Initialize the log.
           Add the Thing to the Thing.objs dict.'''
        super(Thing, self).__init__(**kwargs)
        self.__initLog__(file_str='inventoryobjects.py', class_str='Thing')
        self.logDebug(f'Thing.__init__(kwargs): {dumps(kwargs, indent=4)}')

        # Handle taking this from a loaded file with a saved container..
        try:
            self._container = kwargs['container']
            self.logDebug(f'self._container set to {self._container}')
        # ..or as a newly created instance without one
        except KeyError:
            self._container = self.selected
            self.logDebug(f'No container provided. Using selection {self.selected}')

        Thing.objs[self.UID] = self
        self.category = 'thing'

    def __repr__(self):
        s = f'<Thing object {self.description}({self.UID})'
        s += f'in {self.container.description}'
        if InventoryObject.debug == True:
            s += f'|{self.widget}'
        return s + '>'

    def delete(self):
        '''Delete references to the instance and call the parent's delete method'''
        InventoryObject.changes_made = True
        del Thing.objs[self.UID]
        super(Thing, self).delete()

    def inContainer(self):
        '''Determine if this Thing is assigned to a Container'''
        if self.container != None:
            return True
        else:
            return False

    def isInside(self):
        '''Return the Container for this Thing'''
        return self.getByUID(self.container)

    def updateWidget(self, grid=None):
        '''Make sure the widget has a DataGrid assigned and the widget category matches the
           grid's. Add the grid if necessary.  Check if the widget needs to be drawn and
           draw if necessary.'''

        # If the Thing has no DataGrid assigned and the category matches, assign it
        self.logDebug(f'{self.description} is checking for a grid: ({self.grid}')
        self.logDebug(f'{self.description} is checking categories for self: {self.category}')
        self.logDebug(f'and for grid: {grid.category}')
        self.logDebug(
            'Eval: if self.grid == None and grid != None and self.category == grid.category:')
        if self.grid == None and grid != None and self.category == grid.category:
            self.logDebug(f'Added {grid} to {self}')
            self.grid = grid
        else:
            self.logDebug(f'No grid was added to {self.description}')

        # If the Thing instance is in the selected Container instance, draw the widget
        self.logDebug(f'Checking if {self.description} needs to be drawn')
        if self.selected != None and self.selected.contains(self) == True:
            self.logDebug(f'Drawing widget {self}')
            self.drawWidget()
        # If the Thing is not in the selected Container, undraw the widget
        elif self.selected != None and self.selected.contains(self) == False:
            self.logDebug(f'Undrawing widget {self}')
            self.undrawWidget()

    @property
    def container(self):
        '''Return the Thing's Container object'''
        # self.logDebug(f'Called container property. Container: {self._container}')
        if isinstance(self._container, str):
            self._container = InventoryObject.getByUID(self._container)
        return self._container

    @container.setter
    def container(self, container):
        '''Assign the container object (or string UID) to self._container and flag a change'''
        self._container = container
        InventoryObject.changes_made = True




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
            self.things = {}

        # Call the parent __init__ method to assign attributes and init the log
        super(Container, self).__init__(**kwargs)
        self.__initLog__(file_str='inventoryobjects.py', class_str='Container')

        # Add the instance to the Container.objs dict and set the category of the object
        Container.objs[self.UID] = self
        self.category = 'container'

    def __repr__(self):
        s = f'<Container object {self.description}({self.UID}) '
        s += f'with {len(self.things)} Thing(s)'
        if InventoryObject.debug == True:
            s += f'|{self.widget}'
        return s + '>'

    def addThing(self, thing):
        '''Add a thing to the container. Turn self.things into a dict if it hasn't been,
           add the Thing to self.things and flag a change'''

        if isinstance(self.things, list):
            self._fixThings()

        self.logDebug(f'Adding a {thing} to self.things')
        thing.container = self
        self.things[thing.UID] = thing
        InventoryObject.changes_made = True

    def delete(self):
        '''Flag a change, fix self.things if necessary, delete any contents and call the
           parent delete method'''
        InventoryObject.changes_made = True

        # Check for and delete any contents
        if self.hasContents():
            if isinstance(self.things, list):
                self._fixThings()
            for UID in self.things:
                self.things[UID].delete()

        # Delete any other references to the Container
        del Container.objs[self.UID]
        super(Container, self).delete()

    def hasContents(self):
        '''Check for contents and return True or False'''
        if len(self.things) > 0:
            return True
        else:
            return False

    def contains(self, obj):
        '''Check if a specific Thing is in the Container and return True or False'''
        if obj.UID in self.things:
            return True
        else:
            return False

    def removeThing(self, thing):
        '''Remove the provided Thing object if it is inside the Container'''
        if thing.UID in self.things:
            InventoryObject.changes_made = True
            thing.updateContainer(None)
            del self.things[thing.UID]

    def updateWidget(self, grid=None):
        '''Make sure the widget has a DataGrid assigned and the widget category matches the
           grid's. Add the grid if necessary.  Check if the widget needs to be drawn and
           draw if necessary.'''

        self.logDebug(f'{self.description} is checking for a grid: ({self.grid})')
        self.logDebug(f'{self.description} is checking CATEGORY for self: {self.category}')
        self.logDebug(f'and for grid: {grid.category}')
        self.logDebug('Eval: if self.grid == None and grid != None and self.category == grid.category:')
        if self.grid == None and grid != None and self.category == grid.category:
            self.logDebug(f'Added {grid} to {self}')
            self.grid = grid
        else:
            self.logDebug(f'No grid was added to {self.description}')

        if self.category == grid.category:
            self.drawWidget()

    def _fixThings(self):
        '''Turn the list of Thing UIDs from a loaded file into references to the Thing objects'''
        things = {}
        for UID in self.things:
            things[UID] = InventoryObject.getByUID(UID)
        self.things = things
