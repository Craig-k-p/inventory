from resources.inventoryobjects import Thing, Container
from resources.utilities import LogMethods
from kivy.logger import Logger

class Selection(LogMethods):
    _history = []
    _last_container = None

    def __init__(self, s):
        '''Create the Selection object and link the Thing or Container object that was selected
           s = InventoryObject instance'''
        # super(Selection, self).__init__()
        self.__initLog__('selection.py', 'Selection')
        self.logDebug(f'New selection')
        self._s = s
        self.logDebug(f'Selected {self._s}')

        # Position important (before append)
        self._deselectPrevious()

        # If this is a Container object, we want to mark it as last selected
        # so we can reselect it when the user creates
        if isinstance(self._s, Container):
            Selection._last_container = self

        # Add this object to the selection history
        Selection._history.append(self)

        # Position important (after append)
        self._selectCurrent()

        # If the history length is too long, delete the oldest selection
        if len(Selection._history) > 20:
            del Selection._history[0]

    def __repr__(self):
        '''A brief description of the object'''
        s = f'<Selection obj {self._s}>'
        return s

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
    def _deselectPrevious(cls):
        '''Call widget.deselect method to visually deselect the previous object for the user'''
        if cls._history == []:
            pass
        else:
            previous_selection = cls.get()
            # If user's previous selection isn't None
            if previous_selection._isInventory():
                previous_selection.getObj().widget.deselect()

    @classmethod
    def _selectCurrent(cls):
        '''Call widget.select method to visually select current object for the user'''
        current_selection = cls.get()
        if current_selection._isInventory():
            current_selection.getObj().widget.select()

    @classmethod
    def get(cls):
        '''Return the most recent selection'''
        if cls._history != []:
            selected = cls._history[-1]  # Returns the last item in the list
            Logger.debug(f'Selection.get()-> selected object: {selected}')
            return selected

    @classmethod
    def getLastContainer(cls):
        '''Return the last container that was selected or raise an error if one wasn't selected'''
        if cls._last_container == None:
            Logger.critical(f'Selection.get()-> No container has been selected yet')
            raise ValueError('No selected container')
        else:
            return cls._last_container

