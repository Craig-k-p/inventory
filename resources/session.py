import datetime
import random

from resources.utilities import LogMethods

''' To Do
        -

        '''


class SessionIO(LogMethods):

    def __init__(self):
        '''Define classes within the __init__ function so we can use the user's name to
        assign custom privileges. Store the class definitions in Session.Thing,
        Session.Container'''

        self.__initLog__(
            file_str=__file__,
            class_str='UserSession'
        )

        self.logInfo('App', 'Created a UserSession instance')
        self._user = None

    def __initMEDocDefs__(self):
        '''Define the instance document definitions. This allows us to customize the user's
        database and collection settings when the ME documents are defined as classes'''

        class PropertyObject(mongoengine.Document):
            '''Basic data that all inventory objects have'''
            description = mongoengine.StringField(required=True)
            created_date = mongoengine.DateTimeField(default=datetime.datetime.now)
            tags = mongoengine.ListField(mongoengine.StringField(max_length=25))
            weight = mongoengine.FloatField(required=True)
            usd_value = mongoengine.FloatField(required=True)

        class Thing(PropertyObject):
            '''Inherits from property object and adds other attributes to create a thing'''
            container_id = mongoengine.ReferenceField('Container ID')
            # attributes = mongoengine.ListField(mongoengine.StringField(max_length=25))
            meta = {
                # self.client = mongoengine.connect(db='inventory_app_db', alias=f'{self.user} core')
                # We must set the alias to match the login above found in UserSession.login
                # From what I understand, this ensures that these objects are written to the
                # correct database
                'db_alias': f'{self.user} core',
                'collection': f'inventory_of_{self.user}'
            }

        class Container(PropertyObject):
            ''' container_type, thing_ids '''
            thing_ids = mongoengine.ListField(mongoengine.ReferenceField('Thing'))
            meta = {
                'db_alias': f'{self.user} core',
                'collection': f'inventory_of_{self.user}'
            }

        self._Thing = Thing
        self._Container = Container


    def Thing(self, **kwargs):
        '''Create a new thing'''
        self.logDebug('DB Ops', 'Creating a thing and saving it to the database')
        self.logDebug('DB Ops', f'{kwargs}')
        return kwargs

    def Container(self, **kwargs):
        '''Create a new container'''
        self.logDebug('DB Ops', 'Creating a container and saving it to the database')
        self.logDebug('DB Ops', f'{kwargs}')
        return kwargs


    def get(self, class_str):
        return []
        '''Return the things or containers in the user's database file'''
        # self.logInfo('__TEST__', f'Session.get called with class_str: {class_str}')
        # ObjectClass = getattr(self, '_' + class_str)
        # self.logInfo('TEST', f'Got {ObjectClass} as ObjectClass')


