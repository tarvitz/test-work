# coding: utf-8
from google.appengine.ext import ndb
from datetime import datetime


class Message(ndb.Model):
    """ simple message model"""
    message_id = ndb.IntegerProperty()
    message_data = ndb.StringProperty()
    created_on = ndb.DateTimeProperty(
        auto_now=True, default=datetime.now,
        required=False
    )