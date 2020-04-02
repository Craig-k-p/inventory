from resources.utilities import LogMethods

class InventoryObject():
    objs = {}
    selected = None
    changes_made = False
    def __init__(
            self,
            UID='0',
            description='A void InventoryObject instance',
            value=0,
            weight=0,
            tags='',
            things=None,
            container=None     ):
        # super(InventoryObject, self).__init__()
        # self.__initLog__(file_str='inventoryobjects.py', class_str='InventoryObject')
        self.UID = UID
        self.description = description
        self.value = value
        self.weight = weight
        self.tags = []
        self.widget = None
        self.grid = None
        self.addTags(tags)
        InventoryObject.objs[UID] = self

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
                c['container'] = obj.UID

            elif isinstance(obj, Container):
                d = data['container']
                d['things'] = list(obj.things.keys())

            else:
                self.logCritical(
                    'There is an unidentified object type in InventoryObject.objs'
                )

            d['description'] = obj.description
            d['value'] = obj.value
            d['weight'] = obj.weight
            d['tags'] = obj.tags

        return data





class Thing(InventoryObject, LogMethods):
    objs = {}
    def __init__(self, kwargs):
        super(Thing, self).__init__(**kwargs)
        self.__initLog__(file_str='inventoryobjects.py', class_str='Thing')

        self._container = kwargs['container']
        Thing.objs[self.UID] = self
        self.category = 'thing'

    def __repr__(self):
        s = f'<Thing object {self.description}({self.UID})'
        s += f'in {self.container.description}>'
        return s

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
        self.logDebug(f'Updating widgets for selected: {self.selected}')
        if self.grid == None and grid != None and self.category == grid.category:
            self.logDebug(f'Added {grid} for {self}')
            self.grid = grid

        if self.selected != None and self.selected.isInside(self) == True:
            self.logDebug(f'Drawing widget {self}')
            self.drawWidget()
        elif self.selected != None and self.selected.isInside(self) == False:
            self.logDebug(f'Undrawing widget {self}')
            self.undrawWidget()

    @property
    def container(self):
        self.logDebug(f'Called container property. Container: {self._container}')
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
        self.things = kwargs['things']
        super(Container, self).__init__(**kwargs)
        self.__initLog__(file_str='inventoryobjects.py', class_str='Container')
        Container.objs[self.UID] = self
        self.category = 'container'

    def __repr__(self):
        s = f'<Container object {self.description}({self.UID}) '
        s += f'with {len(self.things)} Thing(s)>'
        return s

    def addThing(self, thing):
        '''Add a thing to the container'''
        thing.updateContainer(self)
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

    def isInside(self, obj):
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
        if self.grid == None and grid != None and self.category == grid.category:
            self.logDebug(f'Added {grid} for {self}')
            self.grid = grid

        self.drawWidget()
