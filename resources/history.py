class History():
    def __init__(self,
                max_length=20,
                default_h=False,
                default_h_walk=True,
                h=[],
                h_walk=[]):
        self.max_length = max_length
        self._h = h
        self._h_walk = h_walk
        self.default_h = False
        self.default_h_walk = True

    def add(self, new_history):
        '''Add a new history item to the history'''
        self._h.append(new_history)
        self._h_walk.append(new_history)
        if isinstance(self.max_length, int):
            # If the self._h is getting too long remove the oldest item
            if len(self._h) >= self.max_length:
                self.deleteOldest()

    def back(self):
        '''Remove the most recent history item and return the previous item
           If there is nothing to return, return None'''
        self.deleteNewest(h=False, h_walk=True)
        return self.getNewest(h=False, h_walk=True)

    def deleteNewest(self, h=None, h_walk=None):
        '''Delete the most recent item added to the history'''
        if h == None:
            h = self.default_h
        if h_walk == None:
            h_walk = self.default_h_walk
        if h == True:
            if len(self._h) > 0:
                del self._h[0]
        if h_walk == True:
            if len(self._h_walk) > 0:
                del self._h_walk[0]

    def deleteOldest(self, h=None, h_walk=None):
        '''Delete the oldest item from the history'''
        if h == None:
            h = self.default_h
        if h_walk == None:
            h_walk = self.default_h_walk
        if h == True:
            if len(self._h) > 0:
                del self._h[0]
        if h_walk == True:
            if len(self._h_walk) > 0:
                del self._h_walk[0]

    def getNewest(self, h=None, h_walk=None):
        '''Return the newest item from the history or None'''
        if h == None:
            h = self.default_h
        if h_walk == None:
            h_walk = self.default_h_walk
        if h == h_walk == True:
            raise Exception("h and h_walk cannot both be True")
        if h_walk == True:
            if len(self._h_walk) > 0:
                return self._h_walk[-1]
            else:
                return None
        elif h == True:
            if len(self._h) > 0:
                return self._h[-1]
            else:
                return None

    def getPrevious(self, h=None, h_walk=None):
        '''Return the second most recent history item or None'''
        if h == None:
            h = self.default_h
        if h_walk == None:
            h_walk = self.default_h_walk
        if h == h_walk == True:
            raise Exception("h and h_walk cannot both be True")
        if h_walk == True:
            if len(self._h_walk) > 1:
                return self._h_walk[-2]
            else:
                return None
        elif h == True:
            if len(self._h) > 1:
                return self._h[-2]
            else:
                return None

    def getOldest(self):
        '''Return the oldest item from the history or None'''
        if len(self._h) > 0:
            return self._h[0]
        else:
            return None

