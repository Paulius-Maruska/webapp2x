#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Various ndb[1] extensions.

[1]: https://developers.google.com/appengine/docs/python/ndb/
"""

import google.appengine.ext.ndb

__author__ = 'Paulius Maruška'

class Model(ndb.Model):
    """ndb.Model[1] extension.
    
    Provides verious useful functions.
    
    In order to override constants used by this class - define the in your subclass. For example:
    
            import google.appengine.ext.ndb
            import webapp2x.ndbx
            
            class User(ndbx.Model):
                _NDBX_PAGE_SIZE = 200 # default page size for User will be overwritten.
                
                country_code = ndb.StringProperty()
                name = ndb.StringProperty()
                email = ndb.StringProperty()
    
    [1]: https://developers.google.com/appengine/docs/python/ndb/modelclass
    """
    _NDBX_PAGE_SIZE = 100
    
    @classmethod
    def count(cls, *query_args, **query_kwargs):
        """Returns a number of records of a specific model. All positional and named arguments are
        passed to ndb.Model.query[1] function.
        
        Warning: DataStore does not have a simple method to count items, so this function requests
        all keys of specific model and counts them. If you have large amounts of records, this
        functions may take a long time to execute and it will do a lot of DataStore API calls.

        Sample:
            import google.appengine.ext.ndb
            import webapp2x.ndbx
            
            class User(ndbx.Model):
                country_code = ndb.StringProperty()
                name = ndb.StringProperty()
                email = ndb.StringProperty()
            
            c_all = User.count()                        # count all users
            c_uk = User.each(User.country_code == 'UK') # iterate through all british users
        
        [1]: https://developers.google.com/appengine/docs/python/ndb/modelclass#Model_query
        """
        if query_args is None:
            query_args = []
        if query_kwargs is None:
            query_kwargs = {}
        count = 0
        query = cls.query(*query_args, **query_kwargs)
        cursor = ndb.Cursor(urlsafe = None)
        more = True
        while more:
            page, cursor, more = query.fetch_page(cls._NDBX_PAGE_SIZE, keys_only = True, start_cursor = cursor)
            count += len(page)
        return count

    @classmethod
    def each(cls, *query_args, **query_kwargs):
        """Generator function, that returns each record of a specific model. All positional and
        named arguments are passed to ndb.Model.query[1] function.

        Warning: If you have large amounts of records, this functions may take a long time to
        execute and it will do a lot of DataStore API calls.
        
        Sample:
            import google.appengine.ext.ndb
            import webapp2x.ndbx
            
            class User(ndbx.Model):
                country_code = ndb.StringProperty()
                name = ndb.StringProperty()
                email = ndb.StringProperty()
            
            # iterate through all users
            for user in User.each():
                pass
            
            # iterate through all british users
            for user in User.each(User.country_code == 'UK'):
                pass
            
            # get a list of all american users
            us_users = list(User.each(User.country_code == 'US'))

        [1]: https://developers.google.com/appengine/docs/python/ndb/modelclass#Model_query
        """
        if query_args is None:
            query_args = []
        if query_kwargs is None:
            query_kwargs = {}
        query = cls.query(*query_args, **query_kwargs)
        cursor = ndb.Cursor(urlsafe = None)
        more = True
        while more:
            page, cursor, more = query.fetch_page(
                cls._NDBX_PAGE_SIZE,
                start_cursor = cursor
            )
            for obj in page:
                yield obj
