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
    clicked = None
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
        self.tags = set()
        self.widget = None
        # self.clicked = self.widget.selected
        self.grid = None
        self.addTags(tags)
        InventoryObject.objs[self.ID] = self

    def addTags(self, tags):
        '''Take a string or list of tags and adds them to self.tags as a list'''
        # Combine the list of tags
        if isinstance(tags, list):
            tags = set(tags)
        elif isinstance(tags, set):
            self.tags = tags | self.tags  # Combine the elements of each set into one set
            self.changes_made = True
        # Turn the string into a list of tags and combine it with tags
        elif isinstance(tags, str) and tags != '':
            tags = self._fixTags(tags)
            self.tags = tags | self.tags  # Combine the elements of each set into one set
            self.changes_made = True

        elif tags == '':
            pass

        else:
            raise ValueError(f'addTags received wrong type: {type(tags)}')

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

    def isSelected(self):
        '''Check if the current object is selected'''
        if InventoryObject.selected == self or InventoryObject.selected == self.ID:
            self.logDebug(f'{self.description} is selected')
            return True
        else:
            self.logDebug(f'{self.description} is not selected')
            return False

    def removeTags(self, tags):
        '''Take a string of user-input tags and remove them from searchable tags'''
        if tags != '':
            tags = self._fixTags(tags)
            self.tags = self.tags - tags
            self.changes_made = True

    def saveNeeded(self):
        '''Return True if a save is needed, False otherwise'''
        if self.changes_made == True:
            return True
        else:
            return False

    def _fixTags(self, tags):
        '''Turn the string of tags into a set of tags'''
        # Remove surrounding blank characters and split the tags up by spaces
        tags = tags.strip()
        tags = set(tags.split(' '))
        # Replace underscores with spaces
        for n in tags:
            n = n.replace('_', ' ')

        return tags

    def undrawWidget(self):
        '''Undraw the widget if it is drawn'''
        if self.widget in self.grid.children:
            self.logDebug(f'Undrawing widget {self.widget}')
            self.grid.remove_widget(self.widget)

    @classmethod
    def changeMade(cls):
        '''Set the changes_made flag for saving data in the future'''
        cls.changes_made = True

    @classmethod
    def checkLoad(cls):
        for ID in cls.objs:
            if isinstance(cls.objs[ID], Thing):
                Logger.debug(f': {cls.objs[ID].description} container: {cls.objs[ID].container}')
            else:
                Logger.debug(f': {cls.objs[ID].description} things: {cls.objs[ID].things}')

    @classmethod
    def debugDump(cls):
        for ID in cls.objs:
            o = cls.objs[ID]
            if isinstance(o, Thing):
                Logger.debug(f'DEBUGING:-Thing - {o.description}---')
                Logger.debug(f'DEBUGING:    ID: {o.ID} t: {type(o.ID)}')
                Logger.debug(f'DEBUGING:    container: {o.container} t: {type(o.container)}')
                Logger.debug(f'DEBUGING:    category: {o.category}')
            else:
                Logger.debug(f'DEBUGING:-Container - {o.description}---')
                Logger.debug(f'DEBUGING:    ID: {o.ID} t: {type(o.ID)}')
                Logger.debug(f'DEBUGING:    category: {o.category}')
                Logger.debug(f'DEBUGING:    contents:')
                for ID in o.things:
                    Logger.debug(f'DEBUGING:        ID: {ID} t: {type(ID)}')

    @classmethod
    def getByID(cls, ID):
        '''Return an object with the give ID (str)'''
        if int(ID) in cls.objs.keys():
            return cls.objs[int(ID)]
        elif str(ID) in cls.objs.keys():
            return cls.objs[str(ID)]
        else:
            s = f'ID {ID} {type(ID)} was not found in InventoryObject.objs'
            s += f'\n{cls.objs.keys()}'
            raise ValueError(s)

    @classmethod
    def getSaveData(cls):
        '''Return a dictionary of json serializable data for saving to a file'''
        data = {
            'thing': {},
            'container': {}
        }
        for ID in cls.objs:
            obj = cls.objs[ID]

            # Save the things
            if isinstance(obj, Thing):
                d = data['thing']
                d[ID] = {}
                d[ID]['container'] = obj.container  # The container's ID

            # Save the containers
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
            d[ID]['tags'] = list(obj.tags)

        return data

    @classmethod
    def getNewID(cls):
        '''Increment cls.ID_counter and return it as a ID'''
        while str(cls.ID_counter) not in cls.objs:
            cls.ID_counter += 1  # Increment the ID counter
            Logger.debug(f':app.ID_counter incremented to {cls.ID_counter}')
            if cls.ID_counter not in cls.objs:
                Logger.debug(f':Returning app.ID_counter {cls.ID_counter}')
                return cls.ID_counter

    # def click(self):
    #     if InventoryObject.clicked != None:
    #         InventoryObject.clicked.declick()
    #     self.clicked = True
    #     InventoryObject.clicked = self

    # def declick(self):
    #     self.clicked = False


    # @classmethod
    # def clicked(cls, clicked):
    #     cls.clicked.clicked = False
    #     cls.clicked = clicked

    @classmethod
    def setBounds(cls, grid, touch):
        '''Set the bounds for each child widget of the grid'''
        for ID in cls.objs:
            if cls.objs[ID].widget in grid.children:
                cls.objs[ID].widget.setBounds()

    @classmethod
    def updateWidgets(cls, grid):
        '''Draw and undraw widgets based on the currently viewed screen'''
        Logger.debug(f': Updating widgets for {cls.selected}')
        for ID in cls.objs:
            if ID not in cls.objs:
                raise KeyError(f'Key {ID} not found in cls.objs')
            try:
                log = f': Updating: {cls.objs[ID]} with container: {cls.objs[ID].container}'
                Logger.debug(log)
            except AttributeError:
                Logger.debug(f': Updating: {cls.objs[ID]}')
            cls.objs[ID].updateWidget(grid)

        Logger.debug(f'DEBUGGER: {InventoryObject.objs}')

    @classmethod
    def wasChanged(cls):
        return InventoryObject.changes_made





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
            self.container = str(self.selected.ID)

        Thing.objs[self.ID] = self
        self.category = 'thing'

    def __repr__(self):
        s = f'<Thing object {self.description} with ID {self.ID}>'
        return s

    def containerDelete(self):
        '''Delete the thing object specifically when the container is deleting its
           contents'''
        container = self.container
        self.container = None
        del Thing.objs[self.ID]
        super(Thing, self).delete()

    def delete(self):
        '''Delete references to the instance and call the parent's delete method'''
        self.changeMade()
        self.logDebug(f'Thing.delete: ID-{self.ID} container-{self.container}')
        # When self.container is deleted, use this to update the container's widgets
        container = self.container
        InventoryObject.getByID(self.container).removeThing(self.ID)
        del Thing.objs[self.ID]
        super(Thing, self).delete()
        InventoryObject.getByID(container).widget.assignValues()

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

    def moveTo(self, destination):
        '''Move the the Thing instance. Accepts a container ID or None as destination'''
        if destination == None:
            self.container = destination
        elif isinstance(destination, (str, int)):
            self.container = destination
        else:
            raise TypeError(f'Recieved the wrong type! ({type(destination)})')


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

        elif self.selected == None:
            pass

        else:
            raise AttributeError('self.updateWidget was unable to resolve choice draw/undraw')


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
        self.content_changed = False

    def __repr__(self):
        s = f'<Container object {self.description} with ID {self.ID} '
        s += f'and {len(self.things)} Thing(s)'
        return s + '>'

    def addThing(self, ID):
        '''Add a thing to the container. Turn self.things into a dict if it hasn't been,
           add the Thing to self.things and flag a change'''
        self.logDebug(f'Adding Thing {ID} to Container {self.ID}')
        self.things.append(str(ID))
        self.contentChanged()
        self.changeMade()

    def delete(self):
        '''Flag a change, fix self.things if necessary, delete any contents and call the
           parent delete method'''
        self.changeMade()

        # Check for and delete any contents
        if self.hasContents():
            self.logDebug(f'hasContents returned True!')
            for ID in self.things:
                InventoryObject.getByID(ID).containerDelete()

        self.logDebug(f'self.things: {self.things}')

        # Delete any other references to the Container
        del Container.objs[self.ID]
        super(Container, self).delete()

    def contentChanged(self):
        '''Set the self.content_changed flag to True'''
        self.content_changed = True

    def contains(self, thing):
        '''Check if a specific Thing or ID is in the Container and return True or False'''
        if isinstance(thing, (int, str)):
            if str(thing) in self.things:
                self.logDebug(f'{self.description} contains {thing} in {self.things}')
                return True
            else:
                self.logDebug(f'{self.description} doesn\'t contain {thing} in {self.things}')
                return False
        elif isinstance(thing, (Thing, Container)):
            if str(thing.ID) in self.things:
                self.logDebug(f'{self.description} contains {thing} in {self.things}')
                return True
            else:
                self.logDebug(f'{self.description} doesn\'t contain {thing} in {self.things}')
                return False
        else:
            raise TypeError(f'Type {type(thing)} not valid. Must be int or str')

    def getValue(self):
        '''Return the total value of the container and its contents'''
        usd_value = float(self.usd_value)
        for ID in self.things:
            usd_value += float(InventoryObject.getByID(ID).usd_value)
            # self.logDebug(ID)
        return int(usd_value)

    def getWeight(self):
        '''Return the total weight of the container and its contents'''
        weight = float(self.weight)
        self.logDebug(f'things {self.things}')
        for ID in self.things:
            weight += float(InventoryObject.getByID(ID).weight)
            self.logDebug(f'ID: {ID}')
        return int(weight)

    def hasContents(self):
        '''Check for contents and return True or False'''
        if len(self.things) > 0:
            return True
        else:
            return False

    def removeThing(self, thing):
        '''Remove the provided Thing object if it is inside the Container'''
        log = f'Container.removeThing: ID-{self.ID} things-{self.things}'
        log += f'\n\tthing-{thing}'
        self.logDebug(log)
        if isinstance(thing, (int, str)):
            if int(thing) in self.things:
                self.changeMade()
                InventoryObject.getByID(thing).container = None
                self.things.remove(int(thing))
                self.widget.assignValues(update=True)
            elif str(thing) in self.things:
                self.changeMade()
                InventoryObject.getByID(thing).container = None
                self.things.remove(str(thing))
                self.widget.assignValues(update=True)

            else:
                raise Exception(f'{thing} {type(thing)} was not deleted')
        else:
            msg = f'Type {type(thing)} not valid. Must be str, int, Thing, or Container'
            raise TypeError(msg)

    def updateWidget(self, grid=None):
        '''Make sure the widget has a DataGrid assigned and the widget category matches the
           grid's. Add the grid if necessary.  Check if the widget needs to be drawn and
           draw if necessary.'''
        if self.content_changed == True:
            self.widget.assignValues(update=True)
            self.content_changed = False

        self.logDebug(f'{self.description} is checking for a grid')
        if self.grid == None and grid != None and self.category == grid.category:
            self.logDebug(f'No grid found. Added to Container {self.ID}')
            self.grid = grid

        if self.category == grid.category:
            self.drawWidget()
        # Containers don't need to be filtered yet.  No need to undraw
        elif self.category != grid.category:
            pass
        else:
            raise AttributeError('self.updateWidget was unable to resolve draw/undraw choice')

        self.widget.setBounds()
