'''
Created on Nov 11, 2013

@author: johannes
'''

class EventHook(object):

    def __init__(self):
        self.__handlers = []

    def __iadd__(self, handler):
        self.__handlers.append(handler)
        return self

    def __isub__(self, handler):
        self.__handlers.remove(handler)
        return self

    def fire(self, *args, **keywargs):
        for handler in self.__handlers:
            handler(*args, **keywargs)

    def clearObjectHandlers(self, inObject):
        for theHandler in self.__handlers:
            if theHandler.im_self == inObject:
                self -= theHandler

class EventHookKeyValue():

    def __init__(self):
        self.clients = {}

    def add(self,string, handler):
        self.clients[string] = handler

    def sub(self, string):
        self.clients.pop(string)

    def fire(self, string):
        self.clients.get(string)()
        