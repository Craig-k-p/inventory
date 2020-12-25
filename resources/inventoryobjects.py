from resources.utilities import LogMethods
from kivy.logger import Logger
from json import dumps


class InventoryObject():
    '''Parent class for inventory objects with base methods and class methods
       that make managing the inventory easier'''

    ID_counter = 0          # Unique ID counter for each of the user's objects
    objs = {}               # All InventoryObject and inherited instances
    _changes_made = False   # Flag to determine whether a save is needed
                            #   It is very important that this is changed using
                            #   InventoryObject.changeMade(), not self.changeMade()
    search_term = ''        # Search term assigned by applySearch method
    clicked = None

    def __init__(
            self,
            ID='0',
            description='A void InventoryObject instance',
            usd_value=0,
            weight=0,
            tags='',
            things=None,
            container=None,
            location=None     ):
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
        self._description = description
        self._usd_value = usd_value
        self._weight = weight
        self._location = location
        self.tags = set()
        self.addTags(tags)
        self._setTagSearchString()
        self.widget = None
        self.data_grid = None
        InventoryObject.objs[self.ID] = self

    @property
    def description(self):
        '''This is called when "self.description" is used in code'''
        return self._description

    @description.setter
    def description(self, description):
        '''This is called when "self.description = 'an example str'" is used in code'''
        # Check for a string type
        if isinstance(description, str):
            # Make sure the string is new and assign it
            if self._description != description:
                self._description = description
                # Flag a change made to the inventory
                InventoryObject.changeMade()
            else:
                self.logDebug(f'"{description}" is already the description')
        else:  # Raise an error if the wrong type is found
            raise TypeError(f'Was expecting type str for desc. Got {type(description)}')

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        '''This is called when "self.location = 'an example str'" is used in code'''
        # Check for a string type
        if isinstance(location, str):
            # Make sure the string is new and assign it
            if self._location != location:
                self._location = location
                # Flag a change made to the inventory
                self.logDebug(f'Location of {self.description} changed to {location}')
                InventoryObject.changeMade()
            else:
                self.logDebug(f'"{location}" is already the location')
        else:  # Raise an error if the wrong type is found
            raise TypeError(f'Was expecting type str for location. Got {type(location)}')

    @property
    def usd_value(self):
        '''This is called when "self.usd_value" is used in code'''
        return self._usd_value

    @usd_value.setter
    def usd_value(self, usd_value):
        '''This is called when "self.usd_value = 123" is used in code'''
        # Check for a string, int, or float type
        if isinstance(usd_value, (str, int, float)):
            self.logDebug(f'{self} usd_value.setter called with value {usd_value}')
            # Make sure the value is new and assign it
            if self._usd_value != usd_value:
                self._usd_value = usd_value
                self.logDebug(f'{usd_value} is a new value. Setting cls._changes_made')
                # Flag a change made to the inventory
                InventoryObject.changeMade()
            else:
                self.logDebug(f'usd_value {usd_value} already saved')
        else:  # Raise an error if str, int, or float was not provided
            raise TypeError(f'Was expecting type str, int, or float for usd_val. Got {type(usd_value)}')

    @property
    def weight(self):
        '''This is called when "self.weight" is used in code'''
        return self._weight

    @weight.setter
    def weight(self, weight):
        '''This is called when "self.weight = 123" is used in code'''
        # Check for a string, int, or float type
        if isinstance(weight, (str, int, float)):
            # assign the value if it is new
            if self._weight != weight:
                self._weight = weight
                # Flag a change made to the inventory
                InventoryObject.changeMade()
        else:
            raise TypeError(f'Was expecting type str, int, or float for weight. Got {type(weight)}')

    def addTags(self, tags):
        '''Take a string or list of tags and adds them to self.tags as a list'''
        # Combine the list of tags
        if isinstance(tags, list):
            tags = set(tags)
            self.tags = tags | self.tags  # Combine the elements of each set into one set
            self._setTagSearchString()
            InventoryObject.changeMade()
        elif isinstance(tags, set):
            self.tags = tags | self.tags  # Combine the elements of each set into one set
            self._setTagSearchString()
            InventoryObject.changeMade()
        # Turn the string into a list of tags and combine it with tags
        elif isinstance(tags, str) and tags != '':
            tags = self._fixTags(tags)
            self.tags = tags | self.tags  # Combine the elements of each set into one set
            self._setTagSearchString()
            InventoryObject.changeMade()

        elif tags == '':
            pass

        else:
            raise ValueError(f'addTags received wrong type: {type(tags)}')

    def delete(self):
        '''Remove the widget and delete the instance from the InventoryObject.objs dict'''
        self.widget.object = None
        self.data_grid.remove_widget(self.widget)
        del InventoryObject.objs[self.ID]

    def drawWidget(self):
        '''Draw the widget if it isn't already'''
        if self.widget not in self.data_grid.children:
            self.logDebug(f'Drawing widget {self.widget}')
            self.data_grid.add_widget(self.widget)

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
            tags = self._fixTags(tags)
            self.tags = self.tags - tags
            InventoryObject.changeMade()

    def undrawWidget(self):
        '''Undraw the widget if it is drawn'''
        if self.widget in self.data_grid.children:
            self.logDebug(f'Undrawing widget {self.widget}')
            self.data_grid.remove_widget(self.widget)

    def _checkSearch(self):
        '''Compare attributes to the search term and return True or False if a match is found'''

        self.logDebug(self.search_term)

        # If there is no search term, return True
        if self.search_term == '':
            return True

        else:
            # If the search term is in the description str return True
            if self.search_term in self.description.lower():
                return True

            # If the search term is in the set of tags return True
            elif self.search_term in self.tag_search_str:
                return True

            elif isinstance(self, Thing):
                self.logDebug(f'Search term not found for {self}')
                return False

            elif isinstance(self, Container):
                if self.search_term in self.location.lower():
                    self.logDebug(F'{self.search_term} WAS found in {self}! Returning TRUE!')
                    return True

                else:
                    self.logDebug(f'{self.search_term} not found in {self}. Return False')
                    return False

    def _checkSearchTags(self):
        '''Searches all tags for a match to the search term'''

        # Join all tags into one string, using a newline between each tag
        tag_str = '\n'.join(self.tags)
        # Make all search_term characters lower case and search the string
        if self.search_term.lower() in tag_str:
            return True
        else:
            return False

    def _fixTags(self, tags):
        '''Turn the string of tags into a set of tags'''

        # Remove surrounding blank characters and split the tags up by spaces
        tags = tags.strip()
        tags = tags.lower()
        tags = set(tags.split(' '))
        return tags

    def _setTagSearchString(self):
        '''Turn the set of tags into a searchable string'''
        if len(self.tags) == 0:
            self.tag_search_str = ''
        else:
            self.tag_search_str = '\n'.join(self.tags)
            self.tag_search_str = self.tag_search_str.replace('_', ' ')

    @classmethod
    def applySearch(cls, search_widget, search_term):
        '''Assign cls.search_term to find matching objects when cls.updateWidgets
           is called'''
        Logger.debug(f'applySearch: Search term "{search_term}" applied')
        search_term = search_term.strip()
        search_term = search_term.lower()

        # Make sure a new search term was provided so we don't waste resources
        if search_term != cls.search_term:
            cls.search_term = search_term
            cls.updateWidgets(cls.app.sm.current_screen.data_grid)

    @classmethod
    def changeMade(cls):
        '''Set the _changes_made class attribute and log the changes'''
        if cls._changes_made == False:
            cls._changes_made = True
            Logger.info(f'INFO: cls._changes_made set to {cls._changes_made}')
        else:
            Logger.debug(f'DEBUG: cls._changes_made is already {cls._changes_made}')

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
        '''Return an object with the given ID (str)'''
        if int(ID) in cls.objs.keys():
            return cls.objs[int(ID)]
        elif str(ID) in cls.objs.keys():
            return cls.objs[str(ID)]
        else:
            s = f'ID {ID} {type(ID)} was not found in InventoryObject.objs'
            s += f'\n.objs: {cls.objs.keys()}'
            Logger.warning(s)
            return None

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
                d[ID]['location'] = obj.location

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

    @classmethod
    def setBounds(cls, data_grid, touch):
        '''Set the bounds for each child widget of the data_grid'''
        for ID in cls.objs:
            if cls.objs[ID].widget in data_grid.children:
                cls.objs[ID].widget.setBounds()

    @classmethod
    def updateWidgets(cls, data_grid):
        '''Draw and undraw widgets based on the currently viewed screen'''
        Logger.debug(f'InvObjs.py: Updating widgets for {data_grid}')

        # Loop through the keys in cls.objs
        for ID in cls.objs:
            if ID not in cls.objs:
                raise KeyError(f'Key {ID} not found in cls.objs')

            try:  # Try to log as a Thing object, otherwise log as a container
                log = f'InvObjs.py: Updating: {cls.objs[ID]} with container: '
                log += f'{cls.objs[ID].container}'
                Logger.debug(log)
            except AttributeError:
                Logger.debug(f'InvObjs.py: Updating: {cls.objs[ID]}')

            # Update widget
            cls.objs[ID].updateWidget(data_grid)

    @classmethod
    def resetChangeMade(cls):
        '''Reset the _changes_made class attribute'''
        cls._changes_made = False

    @classmethod
    def wasChangeMade(cls):
        '''Returns cls._changes_made'''
        return cls._changes_made


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
            self.container = str(self.app.Selection.getLastContainer().getObj().ID)

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
        InventoryObject.changeMade()
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

    def moveTo(self, destination):
        '''Move the the Thing instance. Accepts a container ID or None as destination'''
        if destination == None:
            self.container = destination
        elif isinstance(destination, (str, int)):
            self.container = destination
        else:
            self.logWarning(f'destination was the wrong type. Got {type(destination)}')
        self.logDebug(f'Moved {self} to container {destination}')


    def updateWidget(self, data_grid=None):
        '''Make sure the widget has a Datadata_grid assigned and the widget category matches the
           data_grid's. Add the data_grid if necessary.  Check if the widget needs to be drawn and
           draw if necessary.'''

        self.logDebug(f'{self.description} is checking for a data_grid')

        # If the Thing has no Datadata_grid assigned and the category matches, assign it
        if self.data_grid == None and data_grid != None and self.category == data_grid.category:
            self.logDebug(f'data_grid not found. Added data_grid to {self.description}')
            self.data_grid = data_grid

        # If the widget doesn't match the search, undraw it
        if self._checkSearch() == False:
            self.undrawWidget()

        else:
            # Get the selection
            selection = self.app.Selection.get(suppress=True)

            # If something is selected and...
            # ...if the last selected container contains this object
            if selection != None and \
            self.app.Selection.getLastContainer().getObj().contains(self) == True:
                # Draw the widget
                self.logDebug(f'Drawing widget for {self}')
                self.drawWidget()

            # If something is selected and...
            # ...if the last selected container does not contain this object
            elif selection != None and \
            self.app.Selection.getLastContainer().getObj().contains(self) == False:
                self.logDebug(f'Undrawing widget for {self}')
                self.undrawWidget()

            elif selection == None:
                pass

            else:
                raise AttributeError('self.updateWidget was unable to resolve choice draw/undraw')


class Container(InventoryObject, LogMethods):
    '''Child class that handles special container methods'''
    objs = {}       # Contains all Container instances
    def __init__(self, kwargs):
        '''Create a container instance, call the parent class __init__ and assign its
           attributes'''

        # self.things is a list ID's for "thing" inventory
        try:  # Handle a loaded file
            self.things = kwargs['things']
        except KeyError:   # Handle a newly created Container
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

    def addThing(self, ID, new_instance=True, merge=False):
        '''Add a thing to the container. Turn self.things into a dict if it hasn't been,
           add the Thing to self.things and flag a change'''
        log = f'Adding {self.app.Selection.get(suppress=True).getObj().description}'
        log += f' to {self.description}'
        self.logDebug(log)
        self.things.append(str(ID))

        if new_instance == False and merge == False:
            log = f'Removing {InventoryObject.getByID(ID)} from '
            log += f'{self.app.Selection.getLastContainer().getObj().description}'
            self.logDebug(log)
            self.app.Selection.getLastContainer().getObj().removeThing(ID)

            thing = InventoryObject.getByID(ID)
            self.logDebug(f'Thing being added to this container: {thing}')
            thing.container = self.ID

            self.app.pop.dismiss()
            InventoryObject.updateWidgets(self.data_grid)

        self.contentChanged()
        InventoryObject.changeMade()

    def delete(self):
        '''Flag a change, fix self.things if necessary, delete any contents and call the
           parent delete method'''
        InventoryObject.changeMade()

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
        for ID in self.things:
            weight += float(InventoryObject.getByID(ID).weight)
        return int(weight)

    def hasContents(self):
        '''Check for contents and return True or False'''
        if len(self.things) > 0:
            return True
        else:
            return False

    def merge(self, destination_id):
        '''Merge the contents of this container into another container. Accepts a destination
        container ID. The calling container instance will be deleted'''

        destination = InventoryObject.getByID(destination_id)

        while len(self.things) > 0:
            thing_id = self.things.pop()

            thing = InventoryObject.getByID(thing_id)
            dest = InventoryObject.getByID(destination_id)

            self.logDebug(f'Merging {thing} into {dest}')

            destination.addThing(thing_id, merge=True)
            InventoryObject.getByID(thing_id).moveTo(destination.ID)

        self.app.pop.dismiss()

    def removeThing(self, thing):
        '''Remove the provided Thing object if it is inside the Container'''
        log = f'Container.removeThing: ID-{self.ID} things-{self.things}'
        log += f'\n\tremoving thing-{thing}'
        self.logDebug(log)
        if isinstance(thing, (int, str)):
            if int(thing) in self.things:
                InventoryObject.changeMade()
                InventoryObject.getByID(thing).container = None
                self.things.remove(int(thing))
                self.widget.assignValues()
            elif str(thing) in self.things:
                InventoryObject.changeMade()
                InventoryObject.getByID(thing).container = None
                self.things.remove(str(thing))
                self.widget.assignValues()

            else:
                raise Exception(f'{thing} {type(thing)} was not deleted')
        else:
            msg = f'Type {type(thing)} not valid. Must be str or int'
            raise TypeError(msg)

    def updateWidget(self, data_grid=None):
        '''Make sure the widget has a data_grid assigned and the widget category matches the
           data_grid's. Add the data_grid if necessary.  Check if the widget needs to be drawn and
           draw if necessary.'''
        if self.content_changed == True:
            self.widget.assignValues()
            self.content_changed = False

        self.logDebug(f'{self.description} is checking for a data_grid')
        if self.data_grid == None and data_grid != None and self.category == data_grid.category:
            self.logDebug(f'No data_grid found. Added {data_grid} to {self.description}')
            self.data_grid = data_grid

        # If the widget doesn't match the search, undraw it
        if self._checkSearch() == False:
            self.undrawWidget()

        else:
            if self.category == data_grid.category:
                self.drawWidget()
            # Containers don't need to be filtered yet.  No need to undraw
            elif self.category != data_grid.category:
                pass
            else:
                raise AttributeError('self.updateWidget was unable to resolve draw/undraw choice')

            self.widget.setBounds()
