import datetime
import mongoengine

from resources.utilities import LogMethods

''' To Do
        -

        '''


class UserSession(LogMethods):

    def __init__(self):
        '''Define classes within the __init__ function so we can use the user's name to assign custom privileges.
           Store the class definisions in Session.Thing, Session.Container'''

        self.__initLog__(
            file_str=__file__,
            class_str=UserSession
        )

        self.logInfo('App', 'Created a UserSession instance')
        self._user = None

    def __initMEDocDefs__(self):
        '''Define the instance document definitions. Thiss allows us to customize the user's database and
           collection settings when the ME documents are defined as classes'''

        class PropertyObject(mongoengine.Document):
            '''Basic data that all inventory objects have'''
            created_date = mongoengine.DateTimeField(default=datetime.datetime.now)
            # acquired_date = mongoengine.DateTimeField(required=True)
            owner = mongoengine.StringField(required=True)
            # tags = mongoengine.ListField(mongoengine.StringField(max_length=25))
            weight = mongoengine.FloatField(required=True)
            value = mongoengine.FloatField(required=True)

            meta = {
                'abstract': True
            }

        # Validation:
        # http://docs.mongoengine.org/guide/document-instances.html#pre-save-data-validation-and-cleaning
        class Thing(PropertyObject):
            '''Inherits from property object and adds other attributes to create a thing'''
            name = mongoengine.StringField(required=True)
            # box_id = mongoengine.ReferenceField('Container')
            # attributes = mongoengine.ListField(mongoengine.StringField(max_length=25))
            meta = {
                'db_alias': f'{self.user} core',
                'collection': f'inventory_of_{self.user}'
            }

        class Container(PropertyObject):
            ''' container_type, thing_ids '''
            container_type = mongoengine.StringField(required=True, max_length=30)
            thing_ids = mongoengine.ListField(mongoengine.ReferenceField('Thing'))
            user = mongoengine.StringField(required=True)
            meta = {
                'db_alias': 'core',
                'collection': f'inventory_of_{self.user}',
            }

        # Use last_login query to check whether the user credentials are correct
        class UserInfoDoc(mongoengine.Document):
            ''' ok '''
            email = mongoengine.StringField()
            username = mongoengine.StringField()
            last_login = mongoengine.DateTimeField(default=datetime.datetime.now)
            meta = {
                'db_alias': 'core',
                'collection': f'inventory_of_{self.user}',
            }

            self.Thing = Thing
            self.Container = Container
            # self.UserInfoDoc = UserInfoDoc

    def createThing(self, **kwargs):
        self.logDebug('DB Ops', 'Creating a thing and saving it to the database')
        new_object = self.Thing(**kwargs)
        new_object.save()

    def createContainer(self, **kwargs):
        self.logDebug('DB Ops', 'Creating a container and saving it to the database')
        new_object = self.Container(**kwargs)
        new_object.save()

    def createUser(self, user, pd):
        '''- use user_administrator with PyMongo.command() to create a user
        - use user_administrator to create a new collection
        - use user_administrator to create a role associated with that collection
        - use appAdmin to assign the role to the user
        Database requirements:
          -A user on the inventory_app_db (not the admin database) with the “userAdmin”
           role (note: This allows this user to set and increase their own permission levels)
          -db.createUser({
                user: "user_administrator",
                pwd: "password",    # Find on LP
                roles:       [         { role: "userAdmin", db: "inventory_app_db" }       ]  })

        ---I think this method could be done by sending a request to a script running on the server
        rather than giving user admin privilidges to the user in code form---

        Collections cannot contain collections within them.  There is no tree structure like a file
        system.  You can reference other collections

        TO DO:
            - Create new user and make sure that it is authorized to write to the database collection'''

        self.logInfo('DB Ops', f'Creating a new user {user}')

        self.user = user

        db = self._getUserAdminClient().inventory_app_db
        self.logCritical('PRINT', f'{db}')

        # --- check that the username doesn't already exitst! --- #

        self.logDebug('DB Ops', f'Creating {self.user}\'s user role')
        # Create a custom role for the user on his/her own collection
        db.command('createRole',
                   f'user_role_{self.user}',
                   roles=[],
                   privileges=[
                       {
                           'resource': {'db': 'inventory_app_db',
                                        'collection': f'inventory_of_{self.user}'},
                           'actions': [
                               'find',
                               'createCollection',
                               'dropCollection',
                               'insert',
                               'update',
                               'remove'
                           ]
                       }
                   ]
                   )

        self.logDebug('DB Ops', f'Creating {self.user} in the DB and assigning them their role')

        # Create the user and assign it the custom role
        print(f'--{self.user} password creation--')
        db.command('createUser',
                   self.user,
                   pwd=pd,
                   roles=[
                       {
                           'role': f'user_role_{self.user}',
                           'db': 'inventory_app_db'
                       }
                   ]
                   )
        return True

        # self.login(user, pd)

    def deleteUser(self):
        '''Delete the user and it's collections'''

        print('\nAre you sure you want to delete everything? [y/n]')
        if input(' > ') is 'y':

            # Raw MongoDB command: db.inventory_of_user.drop()
            self.client.inventory_app_db[f'inventory_of_{self.user}'].drop()

            client = self._getUserAdminClient()

            # https://docs.mongodb.com/manual/reference/method/db.collection.drop/#db-collection-drop
            # List of all commands: https://docs.mongodb.com/manual/reference/command/
            # Delete the user's custome role
            client.inventory_app_db.command(
                'dropRole',
                f'user_role_{self.user}'
            )

            # https://docs.mongodb.com/manual/reference/method/db.collection.drop/#db-collection-drop
            # List of all commands: https://docs.mongodb.com/manual/reference/command/
            # Delete the user
            client.inventory_app_db.command(
                'dropUser',
                self.user
            )

    def login(self, user, pd):
        '''Log the user in to the server using username and password.  Save the client session as self.user'''
        self.user = user

        # Check if the user exists

        self.logDebug('DB Ops', f'Attempting to log {self.user} into the database')
        # This actually creates a PyMongo.MongoClient instance
        # The same as pymongo.MongoClient(f'mongodb://user:pwd@ip:port/db_name')
        self.client = mongoengine.connect(db='inventory_app_db',
                                          username=self.user,
                                          password=pd,
                                          host='10.0.0.8',
                                          port=27017,
                                          alias=f'{self.user} core'
                                          )

        self.logInfo('DB Ops', 'UserSession.login executed')

    def _getUserAdminClient(self):
        '''Get the client connection with user admin privilidges to add/delete users'''

        usern = 'user_administrator'
        pswd = 'iamthecreatorandthedestroyerofyouraccess'
        app_db = 'inventory_app_db'
        db_ip = '10.0.0.8'
        db_port = '27017'

        '''
        #https://docs.mongodb.com/manual/reference/built-in-roles/#userAdmin
        #Create a role on the server for the user administrator:
        db.createRole({role: 'inventoryAppUserAdmin',
           roles: [{role: 'userAdmin', db: 'inventory_app_db'}],
           privileges: [
               {resource: {db: 'inventory_app_db', collection: ''}, actions: [
                   'createCollection',
                   'dropCollection',
                   'insert']}
           ]
           }
          )


        #To revoke roles from the user:
        db.runCommand({revokeRolesFromUser: 'user_administrator',
                       roles: [
                           {role: 'userAdmin', db: 'inventory_app_db'}
                       ]
                       }
                      )

        #To grant a role to an existing user use the following command:
        db.grantRolesToUser(
          "user_administrator",
          [
            { role: "userAdmin", db: "inventory_app_db" }
          ]
        )'''

        # PyMongo library can be used similarly
        user_admin_client = mongoengine.connect(
            host=f'mongodb://{usern}:{pswd}@{db_ip}:{db_port}/{app_db}'
        )
        print(user_admin_client)

        return user_admin_client

    # Anytime the user property is changed, the
    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, new_value):
        self._user = new_value
        self.__initMEDocDefs__()


if __name__ == '__main__':
    a = UserSession(input('username: '))
    a.createThing(name='hat', owner=a.user)
    input('---continue---')
    a.deleteUser()
