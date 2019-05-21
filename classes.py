''' Manage inventory for items and keep track of their value

        Improvements for future programs could include:
            -Creating a base class with attributes like weight, value, and ID
            -Creating a single log instance for each file with it's own file
             handler in a less messy kind of way
            -Storing instance attributes in dictionaries for easier transference,
             processing, and scaling
'''
import json
import logging
import datetime

'''
Debug:  Detailed information for debugging purposes
Info:  Confirmation that things are working as expected
Warning:  Indication that something unexpected happened or there is a potential problem in the future: Disk space low
Error:  Due to a serious problem, the software failed to complete a function
Critical:  A problem likely to cause the program to stop working
'''
now = datetime.datetime.now()
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

formatter = logging.Formatter(f'{now.hour}:{now.minute}:%(levelname)s:%(name)s:%(lineno)s:%(message)s')

file_handler = logging.FileHandler(f'logs/classes.{now.day}.{now.month}.{now.year}.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class Inventory():

    '''
    A class that contains information about Box ownership, location, total weight, and total value.
    -Class variable Inventories points to all Inventory objects in existence with the owner's name as a key.
    -Class variable boxes_not_in_inventory points to all Box objects that are not referenced by a specific Inventory object
    '''

    Inventories = {}
    boxes_not_in_inventory = {}

    def __init__(self, owner=None, Boxes={}):
        '''
        Create an Inventory instance
        owner -> string
        Boxes -> {ID_int: Box_obj}
        '''
        logger.info(f'Instantiated a new Inventory object with name {owner}')
        self.owner = owner
        self.Boxes = Boxes
        self._value = 0
        self._weight = 0
        Inventory.Inventories[self.owner] = self
        logger.debug(f'Inventory created for {self.owner}')

    def addExistingBox(self, box_ID):
        '''
        Add a box to the Inventory object from objects that already exist in Inventory.boxes_not_in_inventory
        box_ID -> int
        '''
        if box_ID in Inventory.boxes_not_in_inventory:
            # Remove the Box from boxes_not_in_inventory using the pop method
            self.Boxes[box_ID] = Inventory.boxes_not_in_inventory.pop(Inventory.not_in_inventory[box_ID])
            logger.debug(f'A Box with the ID of {box_ID} was added to Inventory_obj.Boxes (dict)')
            self._updateValues()
        else:
            logger.warning(f'No box ID of {box_ID} was found in Inventory.boxes_not_in_inventory (dict)')

    def addNewBox(self, box_obj):
        '''
        Add a newly created box into this Inventory's pool of boxes
        box_obj -> instance of Box class
        '''
        self.Boxes[box_obj.getID()] = box_obj

    def deleteBox(self, box_ID):
        '''
        Delete a Box obj and it's contents.  Update Inventory obj attributes if necessary
        box_ID = Box obj ID as int
        '''
        if box_ID in self.Boxes.keys():
            self.Boxes[box_ID].destroy()
            logger.debug(f'Box with ID of {box_ID} was destroyed')
            self._updateValues()
        elif box_ID in Inventory.boxes_not_in_inventory.keys():
            Inventory.boxes_not_in_inventory[box_ID].destroy()
        else:
            logger.warning(f'No box with an ID of {ID} was found to destroy')

        logger.debug(f'Permanently deleted box {box_ID} and its contents')

    def getOwner(self):
        '''
        Return the owner's name as a string
        '''
        return self.owner

    def getSaveData(self):
        '''
        Get all necessary Inventory object information to save and recreate the object.  Return a dictionary of the save data.
        '''
        save_data_dict = {
            'owner': self.owner,
            # Get the box IDs in self.Boxes using a list comprehension
            'box IDs': [self.Boxes[x].getID() for x in self.Boxes.keys()]
        }
        logger.info(f'Created save_data_dict for Inventory owned by {self.getOwner()}')
        return save_data_dict

    def getValue(self):
        '''
        Return the total value of the inventory as an integer or a float
        '''
        self._updateValues()
        logger.debug(f'Inventory_obj._value updated to {self._value}')
        return self._value

    def getWeight(self):
        '''
        Return the total weight of the inventory as an integer or a float
        '''
        self._updateValues()
        logger.debug(f'Inventory_obj._weight updated to {self._weight}')
        return self._weight

    def hasBox(self, ID):
        if ID in self.Boxes.keys():
            return True
        else:
            return False

    def loadSavedBox(self, box_data):
        '''
        Create a new Box object in the Inventory's Boxes dictionary as {key: New Box}
        This is a useful method for loading stored data
        B -> dict of box data
        '''

        new_box = Box.fromSaveData(box_data, self)
        self.Boxes[new_box.getID()] = new_box
        logger.info(f'A new box was created with an ID of {new_box.getID()}')

    def removeBox(self, ID):
        '''
        Remove the Box from this Inventory object's Boxes dictionary and put it into the Inventory class dictionary boxes_not_in_inventory
        '''
        self._updateValues()
        self.Boxes[ID].moveToInventory(None)
        logger.debug(f'Removed box {ID} from {self.getOwner()}\'s inventory')

    def requestDeletion(self, box):
        '''
        Delete all references to the Box object passed into this method
        '''
        ID = box.getID()
        count = 0
        if ID in self.Boxes.keys():
            del self.Boxes[ID]
            count += 1
        if ID in Inventory.boxes_not_in_inventory.keys():
            del Inventory.boxes_not_in_inventory[ID]
            count += 1
        if count == 0:
            logger.warning(f'Attempted to delete references to a Box object with the ID of {ID}.  Box not found.')
        elif count > 1:
            logger.warning(f'Deleted a Box object with the ID of {ID} that was found in multiple containers')
        logger.info(f'Deleted Box object with the ID of {ID}')

    @classmethod
    def hasBoxes(cls):
        '''
        Return True if there are box objects with or without inventory ownership.  Return
        False if no box objects exist
        '''
        if len(cls.boxes_not_in_inventory.keys()) is not 0:
            return True
        for key in cls.Inventories.keys():
            if len(cls.Inventories[key].Boxes.keys()) is not 0:
                return True

    @classmethod
    def resetClassAttributes(cls):
        cls.boxes_not_in_inventory = {}
        cls.Inventories = {}

        # If no boxes were found above return False
        return False

    def _updateValues(self):
        '''
        Update the _weight and _value attributes of this Inventory object by summing it's
        Box objects' _weight and _value attributes
        '''
        self._value = 0
        self._weight = 0
        for key in self.Boxes.keys():
            self._value += self.Boxes[key].getValue()
            self._weight += self.Boxes[key].getWeight()
        logger.info(f'Value and weight info for {self.getOwner()}\'s inventory updated')


class Box():

    '''
    A class designed to organize information for boxes or other containers such as their weight, value, contained weight and value,
    ID, Inventory object reference, and Thing object references.
    -class variable Boxes references all Box objects in existence
    -class variable things_not_in_box references all Thing objects not referenced by a Box object
    -class variable IDer keeps track of Box ID's used
    -class variable defaults helps with assigning default variable information when the user doesn't input anything
    '''

    Boxes = {}
    things_not_in_box = {}
    IDer = 0
    defaults = {'weight': 5, 'location': 'Home', 'value': 9.97}

    def __init__(self, location=None, box_weight=None, box_value=None, Inventory=None, ID=None, date_acquired=(now.month, now.year)):
        '''
        Create a Box object instance
        location -> string
        box_weight -> int or float
        box_value -> int or float
        Inventory -> Inventory obj
        ID -> int
        test -> boolean
        '''
        logger.info(self)
        s1 = f'Instantiated a new Box with location: {location}, weight:'
        s2 = ' {box_weight} lbs, value: ${box_value}, Inventory: {Inventory}\'s, ID: {ID}'
        logger.info(s1 + s2)

        # Assign the ID if needed
        self._ID = ID
        if isinstance(self._ID, int) is False:
            self._assignID()

        self.Things = {}
        self._inventory = Inventory
        self.date_acquired = date_acquired
        Box.Boxes[self._ID] = self

        # Assign the default location if needed
        if location is None:
            self._location = Box.defaults['location']
        else:
            self._location = location

        # if the box has no weight or isn't a number
        if box_weight is None or type(box_weight) not in (type(float()), type(int())):
            self.box_weight = Box.defaults['weight']
        else:
            self.box_weight = box_weight

        # If the box wasn't assigned a value set it as the default value
        if box_value is None or type(box_value) not in (type(float()), type(int())):
            self.box_value = Box.defaults['value']
        else:
            self.box_value = box_value

        self._value = None
        self._weight = None

        s1 = f'New Box object attributes updated to location: {self.getLocation()},'
        s2 = f' weight: {self.box_weight} lbs, value: ${self.box_value}, Inventory: '
        s3 = f'{Inventory.getOwner()}\'s, ID: {ID}, totalweight: {self.getWeight()}, '
        s4 = f'totalvalue: {self.getValue()}, Things: {self.Things}'
        logger.info(s1 + s2 + s3 + s4)

    @classmethod
    def fromSaveData(cls, B, I):
        return cls(B['location'], float(B['box weight']), float(B['box value']), I, B['ID'])

    def addThing(self, thing=None):
        '''
        Add a thing object to the Box object's dictionary self.Things
        thing = Thing object OR None
        thing_ID = integer or None
        '''
        if thing.getID() in self.Things.keys():
            logger.warning(f'Thing object with ID {thing_ID} was already in self.Things dictionary')
            return
        elif isinstance(thing, Thing):
            self.Things[thing.getID()] = thing
            logger.info(f'Thing with ID {thing.getID()} added to self.Things')
        # elif isinstance(thing_ID, type(None)) is False: #and thing_ID in Box.things_not_in_box.keys():
        #     self.Things[thing_ID] = Box.things_not_in_box.pop(thing_ID)
        #     logger.info(f'Thing with ID {thing_ID} was added to self.Things from Box.things_not_in_box')
        else:
            logger.error(f'No valid Thing object was provided.  Got {thing}')
            raise(f'No valid thing provided to Box.addThing.  thing = {str(thing)}')

    def moveToInventory(self, new_inventory):
        '''
        Move the Box object to a new inventory, no inventory, or removes it from inventory.  Remove references from the old inventory
        new_inventory -> None OR 'trash' OR Inventory object
        '''
        old_inventory = self.getInventory()
        ID = self.getID()

        if new_inventory is None:
            new_inventory = Inventory.boxes_not_in_inventory

        # If a BOX is being given an inventory from not having one...
        if isinstance(new_inventory, Inventory) and old_inventory == Inventory.boxes_not_in_inventory:
            new_inventory.Boxes[ID] = old_inventory.pop(ID)
            self._inventory = new_inventory
            logger.debug(f'Box object {self.getID()}\'s inventory was changed to boxes_not_in_inventory')

        # If the BOX is being removed from an INVENTORY with no destination INVENTORY...
        elif new_inventory is Inventory.boxes_not_in_inventory and isinstance(old_inventory, Inventory):
            Inventory.boxes_not_in_inventory[ID] = old_inventory.Boxes.pop(ID)
            self._inventory = new_inventory
            logger.debug(f'Box object {self.getID()} was moved to Inventory.boxes_not_in_inventory')

        # If the BOX is being moved to a new INVENTORY....
        elif isinstance(new_inventory, Inventory()) and isinstance(old_inventory, Inventory()):
            # if type(old_inventory) is type(Inventory()):
            new_inventory.Boxes[ID] = old_inventory.Boxes.pop(ID)
            self._inventory = new_inventory
            logger.debug(f'Box object {self.getID()} was moved to {self.getInventory().getOwner()}\'s Inventory')
        elif new_inventory == 'trash':
            del self.getInventory().Boxes[self.getID()]
            self._inventory = None
            logger.debug(f'Box object {self.getID()} severed both references between it\'s inventory and itself')
        else:
            logger.error(f'Unexpected input --{new_inventory} of type {type(new_inventory)}-- for Box.moveToInventory()')
            logger.error('Box object not moved')

    def deleteThing(self, thing):
        '''
        Delete a Thing object
        thing_ID -> Integer
        '''
        logger.info(f'Deleting {Thing.easyID(thing)}...')
        thing.destroy()
        self._updateValues()

    def destroy(self, keep_contents=False):
        '''
        Delete this instance along with all pointers to and from this instance
        keep_contents -> boolean
        '''
        logger.debug(f'{self.easyID(self)} is being destroyed. Contents too?: {keep_contents}')

        if keep_contents is False:
            # Create a list of keys to prevent "Dictionary changed size during iteration" error
            keys = list(self.Things.keys())
            for key in keys:
                self.Things[key].destroy()
        elif keep_contents is True:
            # Combine dictionaries, overwriting any duplicate keys in the first provided dict
            Box.things_not_in_box = {**Box.things_not_in_box, **self.Things}

        if isinstance(self.getInventory(), Inventory) is True:
            self.getInventory().requestDeletion(self)
        elif self.getInventory() is Inventory.boxes_not_in_inventory:
            Inventory().requestDeletion(self)

        del Box.Boxes[self._ID]
        del self._inventory
        del self.Things
        del self._location
        del self.box_value
        del self.box_weight
        del self._value
        del self._weight
        del self._ID
        logger.debug(f'Box destroyed')
        del self

    def getContents(self):
        return self.Things

    def getDateAcquired(self):
        return f'{self.date_acquired[0]}/{self.date_acquired[1]}'

    def getLocation(self):
        return self._location

    def setLocation(self, location_str):
        if isinstance(location_str, str) is True:
            self._location = location_str
        else:
            logger.error('Recieved incorrect type for location.  Need string as input.')

    def getID(self):
        return self._ID

    def getIDerValue(self):
        return Box.IDer

    def getInventory(self):
        return self._inventory

    def getSaveData(self):
        '''
        Get all necessary information to recreate this instance
        '''
        save_data_dict = {
            'ID': self.getID(),
            # Get thing object IDs into a list using a list comprehension
            'thing IDs': [self.Things[x].getID() for x in self.Things.keys()],
            'inventory owner': self.getInventory().getOwner(),
            'location': self.getLocation(),
            'box weight': self.box_weight,
            'box value': self.box_value,
            'date acquired': self.getDateAcquired()
        }
        return save_data_dict

    def getValue(self):
        '''Update the Box instance values and return it's value'''
        self._updateValues()
        return self._value

    def getWeight(self):
        '''Update the Box instance values and return it's weight'''
        self._updateValues()
        return self._weight

    def newThing(self, *args):
        '''
        Create a new Thing instance and capture it's information
        Helpful for recreating save data
        *args -> any number of arguments required by the Thing __init__ method
        '''
        new_thing = Thing(*args)
        self.Things[new_thing.getID()] = new_thing
        logger.debug(f'A new thing was created with an ID of {new_thing.getID()}')
        return new_thing

    def removeThing(self, thing):
        '''
        Remove a Thing object from this Box instance
        ID -> integer
        '''
        # self._value -= self.Things[ID].getValue()
        # self._weight -= self.Things[ID].getWeight()
        thing.putInto(None)
        self._updateValues()
        logger.debug(f'Removed a {Thing.easyID(thing)} from the box')

    @classmethod
    def requestDeletion(cls, thing):
        '''
        Delete a Thing object from this Box instance if present.  Delete it from Box.things_not_in_box if present as well
        container -> None or Box object
        thing -> Thing object
        '''
        ID = thing.getID()
        container = thing.getContainer()

        if container is None:
            del cls.things_not_in_box[ID]

        elif isinstance(container, Box) is True:
            count = 0
            if ID in container.Things.keys():
                del container.Things[ID]
                count += 1
            if ID in Box.things_not_in_box.keys():
                del Box.things_not_in_box[ID]
                count += 1
            if count > 1:
                logger.warning(f'{Thing.easyID(thing)} was found and deleted from two separate dictionaries')
            elif count == 0:
                logger.warning(f'{Thing.easyID(thing)} was not found in any dictionaries')
            else:
                logger.debug(f'{Thing.easyID(thing)} was deleted from the container')

        else:
            raise ValueError(
                f'Box.requestDeletion was expecting Box instance or None from Thing.getContainer(). Got {type(container)}'
            )

    def moveTo(self, location):
        '''
        Set a new location for the Box object
        location -> string
        '''
        self._location = location
        logger.debug(f'The Box\'s location was set to {self.getLocation()}')

    def _assignID(self):
        '''
        Assign the ID for a new Box instance
        '''
        if self._ID is None:
            Box.IDer += 1
            self._ID = Box.IDer
            return self._ID
        else:
            logger.warning(f'{Box.easyID()} already has an ID')

    def _updateValues(self):
        '''
        Update the value and weight of this Box instance and it's contents
        '''
        self._weight = self.box_weight
        self._value = self.box_value
        for key in self.Things.keys():
            self._value += self.Things[key].getValue()
            self._weight += self.Things[key].getWeight()

    @classmethod
    def getBox(cls, ID):
        if ID in cls.Boxes.keys():
            return cls.Boxes[ID]
        else:
            return False

    @classmethod
    def getDefault(cls, key):
        '''
        Get the default value for a specified key
        key -> string
        '''
        return cls.defaults[key]

    @classmethod
    def easyID(cls, ref):
        if ref.getInventory() is Inventory.boxes_not_in_inventory:
            return f'Box obj [ID of {ref.getID()} - no Inventory]'
        else:
            inventory_owner = ref.getInventory().getOwner()
            return f'Box obj [ID of {ref.getID()} in {inventory_owner}\'s Inventory]'

    @classmethod
    def resetClassAttributes(cls):
        cls.Boxes = {}
        cls.IDer = 0
        cls.things_not_in_box = {}


class Thing():

    Things = {}
    IDer = 0
    defaults = {
        'weight': 1,
        'value': 1,
        'name': 'obscure object'
    }

    def __init__(self, name=None, value=None, weight=None, container=None, ID=None, date_acquired=(now.month, now.year)):
        '''
        Create a Thing object instance
        name -> string
        value -> int or float
        weight -> int or float
        container -> Box obj
        ID -> int
        test -> boolean
        '''
        istr = f'Instantiated a new Thing with name: {name}, value: ${value}, '
        istr += f'weight: {weight} lbs, container: {container}, ID: {ID}'
        logger.info(istr)
        self._name = name
        self._value = value
        self._weight = weight
        self.date_acquired = date_acquired

        # Assign the ID if needed
        self._ID = ID
        if isinstance(self._ID, int) is not True:
            self._assignID()

        Thing.Things[self._ID] = self
        self._checkDefaults()
        self._container = container

        # If it has no container add it to the not in box dictionary
        if self._container is None:
            Box.things_not_in_box[self.getID()] = self
            self._container = Box.things_not_in_box

        logger.info(f'{Thing.easyID(self)} attributes updated to value: {self.getValue()}, weight: {self.getWeight()}')

    def destroy(self):
        '''Delete the Thing instance and all references to and from it'''
        del Thing.Things[self.getID()]
        if isinstance(self.getContainer(), Box):
            self.getContainer().requestDeletion(self)
        elif self.getContainer() is None:
            Box.requestDeletion(self)

        else:
            logger.error(f'Thing.getContainer() returned unexpected value: {self.getContainer()}')

        del self._name
        del self._value
        del self._weight
        self.putInto('trash')
        del self._ID
        del self

    def getDateAcquired(self, copy=False):
        if copy is True:
            return self.date_acquired
        else:
            return f'{self.date_acquired[0]}/{self.date_acquired[1]}'

    def getID(self):
        return self._ID

    def getIDerValue(self):
        return Box.IDer

    def getName(self):
        return self._name

    def getValue(self):
        return self._value

    def getWeight(self):
        return self._weight

    def getContainer(self):
        if self.hasContainer():
            return self._container
        else:
            return None

    def hasContainer(self):
        '''Return a boolean or None if this Thing has a container object assigned to self.container'''
        if self._container == Box.things_not_in_box:
            return False
        elif self._container is None:
            logger.error(f'''{self.getName()}'s._container should not be None!''')
            raise ValueError('self.getContainer() should not return None!')
        elif self._container != Box.things_not_in_box and isinstance(self._container, Box):
            return True
        else:
            logger.error(f'Unexpected error > Thing.hasContainer() > self.getContainer() = {self._container}')
            raise ValueError(f'Unexpected error > Thing.hasContainer() > self.getContainer() = {self._container}')
            # return False

    def putInto(self, new_container):
        '''
        Change the container for this Thing instance
        new_container -> None OR Box obj OR 'trash'
        '''
        old_container = self.getContainer()
        if old_container is None:
            old_container = Box.things_not_in_box
        ID = self.getID()

        # If the item is being removed from a container with no destination container
        if new_container in (None, Box.things_not_in_box) and old_container is not Box.things_not_in_box:
            Box.things_not_in_box[ID] = old_container.Things.pop(ID)
            self._container = Box.things_not_in_box

        # If the item is being moved to a new container....
        elif isinstance(new_container, Box):

            # ....from having no container
            if old_container is Box.things_not_in_box:
                new_container.Things[ID] = Box.things_not_in_box.pop(ID)
                self._container = new_container
            # ....from an old container
            elif isinstance(old_container, Box):
                new_container.Things[ID] = old_container.Things.pop(ID)
                self._container = new_container
            else:
                logger.error(f'{Thing.easyID(self)} was not found in things_not_in_box or in the old container.')
                logger.error('Move not completed')

        elif new_container == 'trash':
            del self._container

        else:
            logger.error(f'Unexpected input --{new_container} of type {type(new_container)}-- for Thing.putInto()')
            logger.error('Move not completed')

    def getSaveData(self):
        '''Get the data required to reconstruct this Thing object and return it as a dictionary'''
        save_data_dict = {
            'name': self.getName(),
            'ID': self.getID(),
            'value': self.getValue(),
            'weight': self.getWeight(),
            'date acquired': self.getDateAcquired()
        }
        if isinstance(self.getContainer(), Box):
            save_data_dict['container ID'] = self.getContainer().getID()
        elif self.getContainer() is None:
            save_data_dict['container ID'] = None
        else:
            logger.warning(f'getSaveData() got unexpected input: {self.getContainer()}')

        return save_data_dict

    def _assignID(self):
        '''Assign an ID to new Thing instances'''
        if self._ID is None:
            Thing.IDer += 1
            self._ID = Thing.IDer
            return self._ID
        else:
            return self._ID

    def _checkDefaults(self):
        '''Check through assigned values upon instantiation to be sure class defaults replace "None" or '' values'''
        if self.getName() in (None, ''):
            self._name = Thing.defaults['name'] + str(self.getID())

        if self.getValue() in (None, '') or self.getValue() < 0:
            self._value = Thing.defaults['value']
        else:
            try:
                self._value = float(self._value)
            except ValueError:
                logger.warning(f'Got bad input for value: {self._value}. Setting to default')
                self._value = Thing.defaults['value']

        if type(self.getWeight()) in (type(int()), type(float())) and self.getWeight() > 0:
            return
        elif self.getWeight() is None or self.getWeight() == '' or self.getWeight() <= 0:
            logger.warning(f'Got bad input for weight: {self.getWeight()}. Setting weight to default')
            self._weight = Thing.defaults['weight']
        else:
            try:
                self._weight = float(self.weight)
            except ValueError:
                logger.warning('Failed to convert weight to type float.  Assigning default')
                self._weight = Thing.defaults['weight']

    @classmethod
    def easyID(cls, ref):
        '''
        Method to easily return human identifiable information about the object in a string
        ref -> Thing obj
        '''
        container = ref.getContainer()
        if container is None:
            container = 'NONE'
        return f'Thing obj [{ref.getName()} w/ID {ref.getID()} in Box {container}]'

    @classmethod
    def resetClassAttributes(cls):
        cls.Things = {}
        cls.IDer = 0


if __name__ == "__main__":
    pass
