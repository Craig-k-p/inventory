from kivy.logger import Logger

from resources.history import History
from resources.inventory import Inventory
from resources.utilities import LogMethods

class Selection(LogMethods):
    _history_length = 50
    _history = History(max_length=_history_length)

    def __init__(self, s):
        '''Create the Selection object and link the Thing or Container object that was selected
           s = InventoryObject instance'''
        # super(Selection, self).__init__()
        self.__initLog__('selection.py', 'Selection')
        self._s = s
        self.logDebug(f'Selected: {self._s}')

        # Position important (before append)
        self._deselect()

        # Add this selection to the history
        Selection._history.add(self)

        # Position important (after append)
        self._select()

    def __repr__(self):
        '''A brief description of the object'''
        return f'<Selection obj {self._s}>'

    def getObj(self):
        '''Return the inventory object that was linked to the selection'''
        return self._s

    def _isInventory(self):
        '''Return True if self._s is an inventory object, False otherwise'''
        if self._s == None:
            return False
        else:
            return True

    @classmethod
    def goBack(cls):
        cls._deselect()
        last = cls._history.back()
        cls._select()
        return last

    @classmethod
    def cleanup(cls):
        '''Delete all selections and their associated inventory when user exits their inventory'''
        cls._history = History(max_length=cls._history_length)

    @classmethod
    def get(cls, suppress=True):
        '''Return the most recent selection'''
        selected = cls._history.getNewest()
        Logger.debug(selected)
        if suppress == False:
            Logger.debug(f'Selection.get()-> selected object: {selected}')
        return selected

    @classmethod
    def getContainer(cls):
        '''Return the last container that was selected or raise an error if one wasn't selected'''
        return cls._history.getPrevious()

    @classmethod
    def _deselect(cls):
        '''Call widget.deselect method to visually deselect the previous object for the user'''
        selection = cls.get()
        # If user's previous selection isn't None
        if selection != None and selection._isInventory():
            selection.getObj().widget.deselect()

    @classmethod
    def _select(cls):
        '''Call widget.select method to visually select current object for the user'''
        selection = cls.get()
        if selection._isInventory():
            selection.getObj().widget.select()

