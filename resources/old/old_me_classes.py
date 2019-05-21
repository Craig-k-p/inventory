'''A file to expand on the mongoengine class-object-documents
        - Each class that inherits from mongoengine.Document is a document structure for MongoDB
        documents
        - If inheriting from a parent class for DNRY or added functionality...
            - The parent class must inherit from mongoengine.Document
            - The parent class meta['abstract'] value must = True in order for new
            documents to be put into the collections set by the child class with
            meta['collection'] = 'collection_name')
        -

    Currently working on:
        - How do I create user documents in the user's collection?
            - Class definitions only happen once
            - The 'collection' selections in the meta dictionary are within the class scope, not
            the instance scope
'''

import datetime
import mongoengine


class User(mongoengine.Document):
    ''' email, name '''
    email = mongoengine.StringField(required=True)
    name = mongoengine.StringField(required=True, max_length=25)
    meta = {
        'db_alias': 'core',
        'collection': 'users',
        'role': 'app_user'
    }


class PropertyObject(mongoengine.Document):
    created_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    # acquired_date = mongoengine.DateTimeField(required=True)
    owner = mongoengine.ReferenceField('User')
    tags = mongoengine.ListField(mongoengine.StringField(max_length=25))
    # weight = mongoengine.FloatField(required=True)
    # value = mongoengine.FloatField(required=True)

    meta = {
        'abstract': True
    }


class Thing(PropertyObject):
    name = mongoengine.StringField(required=True)
    box_id = mongoengine.ReferenceField('Container')
    attributes = mongoengine.ListField(mongoengine.StringField(max_length=25))
    meta = {
        'db_alias': 'core',
        'collection': f'inventory_of_.things'
    }


class Container(PropertyObject):
    ''' container_type, thing_ids '''
    container_type = mongoengine.StringField(required=True, max_length=30)
    thing_ids = mongoengine.ListField(mongoengine.ReferenceField('Thing'))
    user = mongoengine.StringField(required=True)
    meta = {
        'db_alias': 'core',
        'collection': f'inventory_of_{user}.containers',
    }


class Version(mongoengine.Document):
    ''' This class could be running on a serverside script and update the
    version as updates occur

    Not currently being used
    Originally intended to create the database by creating a single document'''
    version = mongoengine.ListField(mongoengine.IntField(), max_length=2)
    meta = {
        'db_alias': 'init'
    }


# class Tester(mongoengine.Document):

db.runCommand({revokeRolesFromUser: 'user_administrator',
               roles: [
                   {role: 'userAdmin', db: 'inventory_app_db'}
               ]
               }
              )
