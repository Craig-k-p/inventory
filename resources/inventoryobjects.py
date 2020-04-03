from resources.utilities import LogMethods
from kivy.logger import Logger
from json import dumps

class InventoryObject():
    debug = True
    # Unique ID for each of the user's objects
    uid_counter = 0
    objs = {}
    selected = None
    changes_made = False
    # last_created = None
    def __init__(
            self,
            UID='0',
            description='A void InventoryObject instance',
            usd_value=0,
            weight=0,
            tags='',
            things=None,
            container=None     ):
        self.UID = UID
        self.description = description
        self.usd_value = usd_value
        self.weight = weight
        self.tags = []
        self.widget = None
        self.grid = None
        self.addTags(tags)
        InventoryObject.objs[self.UID] = self
        # InventoryObject.last_created = self

    def addTags(self, tags):
        '''Take a string of user-input tags and turn them into a list of searchable tags'''
        if isinstance(tags, list):
            self.tags += tags
            self.changes_made = True
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
        self.widget.object = None
        self.grid.remove_widget(self.widget)
        del InventoryObject.objs[self.UID]

    def drawWidget(self):
        if self.widget not in self.grid.children:
            self.logDebug(f'Adding widget {self.widget}')
            self.grid.add_widget(self.widget)

    def hasParent(self):
        if self.widget != None:
            if self.widget.parent != None:
                return True
        return False

    def hasWidget(self):
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
        if self.widget in self.grid.children:
            self.logDebug(f'Removing widget {self.widget}')
            self.grid.remove_widget(self.widget)

    def saveNeeded(self):
        if self.changes_made == True:
            return True
        elif self.changes_made == False:
            return False
        else:
            raise Exception(f'self.changes_made was unexpected: {self.changes_made}')

    @classmethod
    def getByUID(cls, UID):
        if UID in cls.objs.keys():
            return cls.objs[UID]
        else:
            return None

    @classmethod
    def getSaveData(cls):
        '''Return a dictionary of json serializable data for safe keeping'''
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
        '''Increment cls.uid_counter and return the usd_value'''

        invalid = True
        while invalid:
            cls.uid_counter += 1  # Increment the ID counter
            Logger.debug(f':app.uid_counter incremented to {cls.uid_counter}')
            if str(cls.uid_counter) not in cls.objs:
                Logger.debug(f':Returning app.uid_counter {cls.uid_counter}')
                return str(cls.uid_counter)

    @classmethod
    def updateWidgets(cls, grid):
        Logger.debug(f': Updating widgets for {cls.selected}')
        for UID in cls.objs:
            Logger.debug(f':Updating: {cls.objs[UID]}')
            cls.objs[UID].updateWidget(grid)





class Thing(InventoryObject, LogMethods):
    objs = {}
    def __init__(self, kwargs):
        super(Thing, self).__init__(**kwargs)
        self.__initLog__(file_str='inventoryobjects.py', class_str='Thing')

        try:
            self._container = kwargs['container']
        except KeyError:
            self._container = self.selected

        Thing.objs[self.UID] = self
        self.category = 'thing'

    def __repr__(self):
        s = f'<Thing object {self.description}({self.UID})'
        s += f'in {self.container.description}'
        if InventoryObject.debug == True:
            s += f'|{self.widget}'
        return s + '>'

    def delete(self):
        InventoryObject.changes_made = True
        del Thing.objs[self.UID]
        super(Thing, self).delete()

    def inContainer(self):
        if self.container != None:
            return True
        else:
            return False

    def isInside(self):
        return self.getByUID(self.container)

    def updateWidget(self, grid=None):
        self.logDebug(f'{self.description} is checking for a grid: ({self.grid}')
        self.logDebug(f'{self.description} is checking categories for self: {self.category}')
        self.logDebug(f'and for grid: {grid.category}')
        self.logDebug('Eval: if self.grid == None and grid != None and self.category == grid.category:')
        if self.grid == None and grid != None and self.category == grid.category:
            self.logDebug(f'Added {grid} to {self}')
            self.grid = grid
        else:
            self.logDebug(f'No grid was added to {self.description}')

        self.logDebug(f'Checking if {self.description} needs to be drawn')
        if self.selected != None and self.selected.contains(self) == True:
            self.logDebug(f'Drawing widget {self}')
            self.drawWidget()
        elif self.selected != None and self.selected.contains(self) == False:
            self.logDebug(f'Undrawing widget {self}')
            self.undrawWidget()

    @property
    def container(self):
        # self.logDebug(f'Called container property. Container: {self._container}')
        if isinstance(self._container, str):
            self._container = InventoryObject.getByUID(self._container)
        return self._container

    @container.setter
    def container(self, container):
        self._container = container
        InventoryObject.changes_made = True




class Container(InventoryObject, LogMethods):
    objs = {}
    def __init__(self, kwargs):
        try:
            self.things = kwargs['things']
        except KeyError:
            self.things = {}
        super(Container, self).__init__(**kwargs)
        self.__initLog__(file_str='inventoryobjects.py', class_str='Container')
        Container.objs[self.UID] = self
        self.category = 'container'

    def __repr__(self):
        s = f'<Container object {self.description}({self.UID}) '
        s += f'with {len(self.things)} Thing(s)'
        if InventoryObject.debug == True:
            s += f'|{self.widget}'
        return s + '>'

    def addThing(self, thing):
        '''Add a thing to the container'''

        if isinstance(self.things, list):
            self._fixThings()

        self.logDebug(f'Adding a {thing} to self.things')
        thing.container = self
        self.things[thing.UID] = thing
        InventoryObject.changes_made = True

    def delete(self):
        InventoryObject.changes_made = True
        del Container.objs[self.UID]
        super(Container, self).delete()

    def hasContents(self):
        if len(self.things) > 0:
            return True
        else:
            return False

    def contains(self, obj):
        if obj.UID in self.things:
            return True
        else:
            return False

    def removeThing(self, thing):
        if thing.UID in self.things:
            InventoryObject.changes_made = True
            thing.updateContainer(None)
            del self.things[thing.UID]

    def updateWidget(self, grid=None):
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
        things = {}
        for UID in self.things:
            things[UID] = InventoryObject.getByUID(UID)
        self.things = things
