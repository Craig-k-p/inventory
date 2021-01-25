from json import dumps

from kivy.logger import Logger

from resources.utilities import LogMethods
from graphics.screens2 import InventoryScreen



class Inventory():
    '''Parent class for inventory objects with base methods and class methods
       that make managing the inventory easier'''

    ID_counter = 0          # Unique ID counter for each of the user's objects
    objs = {}               # All Inventory and inherited instances
    search_term = ''        # Search term assigned by applySearch method
    clicked = None
    _tag_counter = {}       # Used to find the most common tags
    _changes_made = False   # Flag to determine whether a save is needed
                            #   It is very important that this is changed using
                            #   Inventory.changeMade(), not self.changeMade()

    def __init__(
            self,
            ID='0',
            description='A void Inventory instance',
            usd_value=0,
            weight=0,
            tags='',
            things=None,
            container=None,
            contents=[]
            ):
        '''Create an instance of Inventory object and assign its ID, description,
           USD value, weight, and tags. Add it to the Inventory.objs dictionary
           Takes input:
           ID - int as a string
           description - string
           usd_value - int as string
           weight - int as string
           tags - single-word or multi-word (separated by _) tags separated by a space
           things - None; to be replaced by contents
           container -  None; holding container for this object'''
        self.__initLog__(file_str='Inventorys.py', class_str='Thing')
        self.ID = ID
        self._description = description
        self._usd_value = usd_value
        self._weight = weight
        self.tags = set()
        self.addTags(tags)
        self._setTagSearchString()
        self.widget = None         # The DataRow instance
        self.parent_widget = None  # The DataGrid instance
        self.popup_widget = None   # The Screen widget for selecting inventory
        self.content_changed = False

        # Handle taking this from a loaded file with a saved container..
        try:
            self.container = kwargs['container']
        # ..or as a newly created instance without one
        except KeyError:
            self.container = str(self.app.selection.getLastContainer().getObj().ID)

        # Create the object's screen
        self.screen = InventoryScreen(self, name=str(self.ID))

        Inventory.objs[self.ID] = self

    def __repr__(self):
        s = f'<Inventory object {self.description} with ID {self.ID}>'
        return s

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
                Inventory.changeMade()
            else:
                self.logDebug(f'"{description}" is already the description')
        else:  # Raise an error if the wrong type is found
            raise TypeError(f'Was expecting type str for desc. Got {type(description)}')

    @property
    def usd_value(self):
        '''This is called when "self.usd_value" is used in code'''
        if self.hasContents():
            usd_value = float(self.usd_value)
            for ID in self.contents:
                usd_value += float(InventoryObject.getByID(ID).usd_value)
            return int(usd_value)
        else:
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
                Inventory.changeMade()
            else:
                self.logDebug(f'usd_value {usd_value} already saved')
        else:  # Raise an error if str, int, or float was not provided
            raise TypeError(f'Was expecting type str, int, or float for usd_val. Got {type(usd_value)}')

    @property
    def weight(self):
        '''This is called when "self.weight" is used in code'''
        if self.hasContents():
            weight = float(self.weight)
            for ID in self.contents:
                weight += float(InventoryObject.getByID(ID).weight)
            return weight
        else:
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
                Inventory.changeMade()
        else:
            raise TypeError(f'Was expecting type str, int, or float for weight. Got {type(weight)}')

    def addInventory(self, ID, new_instance=True, merge=False):
        '''Add Inventory to self.contents. Turn self.contents into a dict if it hasn't been,
           add the Inventory to self.contents and flag a change'''
        moving_inventory = Inventory.getByID(ID)
        old_container = Inventory.getByID(moving_inventory.container)
        self.contents.append(str(ID))

        if new_instance == False and merge == False:
            log = f'Removing {moving_inventory} from {old_container.description}'
            self.logDebug(log)
            old_container.removeInventory(ID)

            self.logDebug(f'Inventory being added to this container: {moving_inventory}')
            moving_inventory.container = self.ID

            self.app.pop.dismiss()
            Inventory.updateWidgets(self.parent_widget)

        self.contentChanged()
        Inventory.changeMade()
        self.widget.assignValues()

    def addTags(self, tags):
        '''Takes tags of string, list, or set type and change self.tags accordingly'''
        if isinstance(tags, list):
            tags = set(tags)
            if self._tagsWereChanged(tags):
                self._addTags(tags)

        elif isinstance(tags, set):
            if self._tagsWereChanged(tags):
                self._addTags(tags)

        # Turn the string into a list of tags and combine it with tags
        elif isinstance(tags, str) and tags != '':
            tags = self._fixTags(tags)
            if self._tagsWereChanged(tags):
                self._addTags(tags)

        elif tags == '':
            pass
        else:
            Logger.warning(f'addTags received wrong type: {type(tags)}')

    def contains(self, content):
        '''Check if Inventory is in the Container and return True or False'''
        if isinstance(content, (int, str)):
            if str(thing) in self.things or int(thing) in self.things:
                # self.logDebug(f'{self.description} contains {content} in {self.contents}')
                return True
            else:
                # self.logDebug(f'{self.description} doesn\'t contain {content} in {self.contents}')
                return False
        elif isinstance(content, Inventory):
            if str(content.ID) in self.things:
                # self.logDebug(f'{self.description} contains {content} in {self.contents}')
                return True
            else:
                # self.logDebug(f'{self.description} doesn\'t contain {content} in {self.contents}')
                return False
        else:
            raise TypeError(f'Type {type(thing)} not valid. Must be int or str')

    def contentChanged(self):
        '''Set the self.content_changed flag to True'''
        self.content_changed = True

    def delete(self):
        '''Remove the widget and delete the instance from the Inventory.objs dict'''
        Inventory.changeMade()
        self.container.deleteContent(self)
        self.widget.object = None
        self.parent_widget.remove_widget(self.widget)

        if self.hasContents() == True:
            for ID in self.contents:
                Inventory.getByID(ID).delete()

        if self.container != None:
            Inventory.getByID(container).widget.assignValues()

        self.container = None

        del Inventory.objs[self.ID]

    def deleteContent(self, obj):
        '''Remove Inventory from contents'''
        if obj.ID in self.contents:
            self.contents.remove(obj.ID)

    def drawWidget(self):
        '''Draw the widget if it isn't already'''
        if self.widget not in self.parent_widget.children:
            # self.logDebug(f'Drawing widget {self.widget}')
            self.parent_widget.add_widget(self.widget)

    def getContainer(self):
        '''Return the Inventory's container'''
        return Inventory.getByID(self.container)

    def getTags(self):
        '''Return a set of tags'''
        return self.tags

    def hasContents(self, count=False):
        '''Check for contents and return True or False'''
        if count == True and isinstance(self.contents, list):
            return len(self.contents)
        elif count == True:
            return 0
        else:
            if isinstance(self.contents, list) and len(self.contents) > 0:
                return True
            else:
                return False

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

    def inContainer(self):
        '''Determine if this Thing is assigned to a Container'''
        if self.container != None:
            return True
        else:
            return False

    def merge(self, destination_id):
        '''Merge the contents of this container into another container. Accepts a destination
        container ID. The calling container instance will be deleted'''

        destination = InventoryObject.getByID(destination_id)

        while len(self.contents) > 0:
            content_id = self.contents.pop()

            content = InventoryObject.getByID(content_id)
            dest = InventoryObject.getByID(destination_id)

            self.logDebug(f'Merging {content} into {dest}')

            destination.addThing(content_id, merge=True)
            InventoryObject.getByID(content_id).moveTo(destination.ID)

        self.app.pop.dismiss()

    def moveTo(self, destination):
        '''Move the the Inventory instance. Accepts ID or None as destination'''
        if destination == None:
            self.container = destination
        elif isinstance(destination, (str, int)):
            self.container = destination
        else:
            self.logWarning(f'Destination was the wrong type. Got {type(destination)}')
            return
        self.logDebug(f'Moved {self} to container {destination}')

    def removeContent(self, content):
        '''Remove the provided Thing object if it is inside the Container'''
        if isinstance(content, (int, str)):
            if int(content) in self.contents:
                InventoryObject.changeMade()
                InventoryObject.getByID(content).container = None
                self.contents.remove(int(content))
                self.widget.assignValues()
            elif str(content) in self.contents:
                InventoryObject.changeMade()
                InventoryObject.getByID(content).container = None
                self.contents.remove(str(content))
                self.widget.assignValues()
            else:
                raise Exception(f'{content} {type(content)} was not deleted')
        else:
            msg = f'Type {type(content)} not valid. Must be str or int'
            raise TypeError(msg)

    def removeTags(self, tags):
        '''Take a string of user-input tags and remove them from searchable tags'''
        if tags != '':
            tags = self._fixTags(tags)
            self.tags = self.tags - tags
            Inventory.changeMade()

    def undrawWidget(self):
        '''Undraw the widget if it is drawn'''
        if self.widget in self.parent_widget.children:
            self.logDebug(f'Undrawing widget {self.widget}')
            self.parent_widget.remove_widget(self.widget)




    def updateWidget(self, parent_widget=None):
        '''Make sure the widget has a parent_widget assigned. Add the parent_widget if necessary.
           Check if the widget needs to be drawn and draw if necessary.'''

        self.logDebug(f'{self.description} is checking for a parent_widget')

        if self.container == None:
            self.parent_widget = self.screen.parent_widget

        # If the Thing has no parent_widget assigned and the category matches, assign it
        if self.parent_widget == None and parent_widget != None:
            self.logDebug(f'parent_widget not found. Added parent_widget to {self.description}')
            self.parent_widget = parent_widget

        # If the widget doesn't match the search, undraw it
        if self._checkSearch() == False:
            self.undrawWidget()

        else:
            # Get the selection
            selection = self.app.selection.get(suppress=True)

            # If something is selected and...
            # ...if the last selected container contains this object
            if selection != None and \
            self.app.selection.getLastContainer().getObj().contains(self) == True:
                # Draw the widget
                self.logDebug(f'Drawing widget for {self}')
                self.drawWidget()

            # If something is selected and...
            # ...if the last selected container does not contain this object
            elif selection != None and \
            self.app.selection.getLastContainer().getObj().contains(self) == False:
                # self.logDebug(f'Undrawing widget for {self}')
                self.undrawWidget()

            elif selection == None:
                pass

            else:
                raise AttributeError('self.updateWidget was unable to resolve choice draw/undraw')

    def updateWidget(self, parent_widget=None):
        '''Make sure the widget has a parent_widget assigned and the widget category matches the
           parent_widget's. Add the parent_widget if necessary.  Check if the widget needs to be drawn and
           draw if necessary.'''
        if self.content_changed == True:
            self.widget.assignValues()
            self.content_changed = False

        # self.logDebug(f'{self.description} is checking for a parent_widget')
        if self.parent_widget == None and parent_widget != None and self.category == parent_widget.category:
            # self.logDebug(f'No parent_widget found. Added {parent_widget} to {self.description}')
            self.parent_widget = parent_widget

        # If the widget doesn't match the search, undraw it
        if self._checkSearch() == False:
            self.undrawWidget()

        else:
            if self.category == parent_widget.category:
                self.drawWidget()
            # Containers don't need to be filtered yet.  No need to undraw
            elif self.category != parent_widget.category:
                pass
            else:
                raise AttributeError('self.updateWidget was unable to resolve draw/undraw choice')

            self.widget.setBounds()




    def _addTags(self, tags):
        '''Add the tags to self.tags and set the changes_made flag to True'''
        self.tags = tags
        self._setTagSearchString()
        Inventory.changeMade()

    def _checkSearch(self):
        '''Compare attributes to the search term and return True or False if a match is found'''

        # self.logDebug(self.search_term)

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

            else:
                return False

    def _checkSearchTags(self):
        '''Searches all tags for a match to the search term'''

        # Join all tags into one string, using a newline between each tag
        tag_str = '\n'.join(self.tags)
        # Make all search_term characters lower case and search the string
        if Inventory.search_term.lower() in tag_str:
            return True
        else:
            return False


        # Join all tags into one string, using a newline between each tag
        tag_str = '\n'.join(self.tags)
        # Make all search_term characters lower case and search the string
        if Inventory.search_term.lower() in tag_str:
            return True

        else:
            if self.hasContents() == True:
                for key in self.contents:
                    self.logDebug('CHECKING FOR LOOP')
                    if Inventory.getByID(key)._checkSearchTags() == True:
                        return True
                # If we haven't returned True we need to return False
                return False
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

    def _tagsWereChanged(self, tags):
        if self.tags == tags:
            return False
        else:
            return True

    @classmethod
    def cleanup(cls):
        '''Cleanup inventory when the user exits their inventory'''
        cls.objs = {}

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
            cls.updateWidgets(cls.app.sm.current_screen.parent_widget)

    @classmethod
    def changeMade(cls):
        '''Set the _changes_made class attribute and log the changes'''
        if cls._changes_made == False:
            cls._changes_made = True
            # Logger.info(f'INFO: cls._changes_made set to {cls._changes_made}')
        # else:
            # Logger.debug(f'DEBUG: cls._changes_made is already {cls._changes_made}')


    @classmethod
    def getByID(cls, ID):
        '''Return an object with the given ID (str)'''
        if int(ID) in cls.objs.keys():
            return cls.objs[int(ID)]
        elif str(ID) in cls.objs.keys():
            return cls.objs[str(ID)]
        else:
            s = f'ID {ID} {type(ID)} was not found in Inventory.objs'
            s += f'\n.objs: {cls.objs.keys()}'
            Logger.warning(s)
            return None

    @classmethod
    def getNewID(cls):
        '''Increment cls.ID_counter and return it as a ID'''
        while str(cls.ID_counter) not in cls.objs:
            cls.ID_counter += 1  # Increment the ID counter
            # Logger.debug(f':app.ID_counter incremented to {cls.ID_counter}')
            if cls.ID_counter not in cls.objs:
                # Logger.debug(f':Returning app.ID_counter {cls.ID_counter}')
                return cls.ID_counter

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
                    ':There is an unidentified object type in Inventory.objs'
                )

            d[ID]['description'] = obj.description
            d[ID]['usd_value'] = obj.usd_value
            d[ID]['weight'] = obj.weight
            d[ID]['tags'] = list(obj.tags)

        return data

    @classmethod
    def getTopTags(cls):
        '''Returns the six most common tags in the inventory'''
        tags_to_return = 6

        for obj in cls.objs:
            tags = cls.objs[obj].tags
            if len(tags) > 0:
                for tag in tags:
                    if tag in cls._tag_counter:
                        cls._tag_counter[tag] += 1
                    else:
                        cls._tag_counter[tag] = 1

        if tags_to_return > len(cls._tag_counter):
            tags_to_return = len(cls._tag_counter)

        top_tags = []

        for n in range(tags_to_return):
            top_tag = max(cls._tag_counter, key=cls._tag_counter.get)
            top_tags.append(top_tag)
            del cls._tag_counter[top_tag]

        if len(top_tags) > 0:
            cls._tag_counter = {}
            return '\n'.join(top_tags)
        else:
            cls._tag_counter = {}
            return 'N/A'

    @classmethod
    def setBounds(cls, parent_widget, touch):
        '''Set the bounds for each child widget of the parent_widget'''
        for ID in cls.objs:
            if cls.objs[ID].widget in parent_widget.children:
                cls.objs[ID].widget.setBounds()

    @classmethod
    def updateWidgets(cls, parent_widget):
        '''Draw and undraw widgets based on the currently viewed screen'''
        Logger.debug(f'InvObjs.py: Updating widgets for {parent_widget}')

        # Loop through the keys in cls.objs
        for ID in cls.objs:
            if ID not in cls.objs:
                raise KeyError(f'Key {ID} not found in cls.objs')

            # Update widget
            cls.objs[ID].updateWidget(parent_widget)

    @classmethod
    def resetChangeMade(cls):
        '''Reset the _changes_made class attribute'''
        cls._changes_made = False

    @classmethod
    def wasChangeMade(cls):
        '''Returns cls._changes_made'''
        return cls._changes_made
