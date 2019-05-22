'''Used to authenticate or create a new user'''
import mongoengine
from getpass import getpass

# If an error occurs such as: Elements in privilege arrays must be objects
# You likely need a Document-style dictionary!


def createUser():
    '''
      - use user_administrator with PyMongo.command() to create a user
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

    I think this method could be done by sending a request to a script running on the server
    rather than giving user admin privilidges to the user.
    '''
    import pymongo

    print('Create a user?')
    response = input(' > ')

    if response == 'y':
        usern = 'user_administrator'
        pswd = 'iamthecreatorandthedestroyerofyouraccess'
        app_db = 'inventory_app_db'

        # This can be used (PyMongo library):
        client = pymongo.MongoClient(f'mongodb://{usern}:{pswd}@10.0.0.8/inventory_app_db')
        # ...Or this from the MongoEngine library (both return a PyMongo.MongoClient):
        # client = mongoengine.connect(db='inventory_app_db',
        #                              username=usern,
        #                              password=pswd,
        #                              host='10.0.0.8',
        #                              port=27017,
        #                              alias='init'
        #                              )

        db = client.inventory_app_db

        username = input('Username: ')
        pswd = getpass()
        # --- check that the username doesn't already exitst! --- #

        db.command('createRole',
                   f'user_role_{username}',
                   roles=[],
                   privileges=[
                       {
                           'resource': {'db': 'inventory_app_db',
                                        'collection': f'inventory_collection_{username}'},
                           'actions': ['find', "createCollection", 'insert', 'update', 'remove']
                       }
                   ]
                   )

        db.command('createUser',
                   username,
                   pwd=pswd,
                   roles=[
                       {
                           'role': f'user_role_{username}',
                           'db': 'inventory_app_db'
                       }
                   ]
                   )


class Session():
    '''Use MongoEngine to log the user in'''

    def __init__(self):
        self.user = input('username: ')

        # This actually creates a PyMongo.MongoClient instance
        # The same as pymongo.MongoClient(f'mongodb://user:pwd@ip:port/db_name')
        self.client = mongoengine.connect(db='inventory_app_db',
                                          username=self.user,
                                          password=getpass(),
                                          host='10.0.0.8',
                                          port=27017,
                                          alias='core'
                                          )


if __name__ == '__main__':
    createUser()
    login()
