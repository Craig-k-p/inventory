import datetime
from resources.utilities import LogMethods


class SessionIO(LogMethods):

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




