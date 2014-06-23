# coding: utf-8
import unittest

from google.appengine.ext import testbed
from google.appengine.ext import ndb

from application import app
from application.models import Message

import simplejson as json

# TODO: RESTful representations require valid HTTP statuses
# fix message create/retrieve/update/delete HTTP like them should be


class MessageTest(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        self.app = app.test_client()

        self.post = {
            'message_id': 1,
            'message_data': 'data'
        }
        self.put = {
            'message_id': 2,
            'message_data': 'data put',
        }

        self.initial = {
            'message_id': 1,
            'message_data': 'message data',
        }

    def tearDown(self):
        self.testbed.deactivate()

    def add_message(self):
        """
        generates new message for tests issues

        :return:
        """
        msg = Message(**self.initial)
        msg.put()
        return msg

    def test_home(self):
        """
        Home page

        :return:
        """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_api_get_message(self):
        msg = self.add_message()
        url = '/api/messages/%s/' % msg.message_id
        response = self.app.get(url, data={}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        load = json.loads(response.data)
        self.assertEqual(load['message_id'], self.initial['message_id'])
        self.assertEqual(load['message_data'], self.initial['message_data'])
        self.assertIn('created_on', load)

    def test_api_post_message(self):
        count = Message.query().count()
        response = self.app.post('/api/messages/', data=self.post,
                                 follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        load = json.loads(response.data)
        self.assertEqual(load['message_id'], self.post['message_id'])
        self.assertEqual(Message.query().count(), count + 1)

    def test_api_delete_message(self):
        msg = self.add_message()
        pk = msg.message_id
        url = '/api/messages/%s/' % pk
        count = Message.query().count()
        response = self.app.delete(url, data={},
                                   follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        key = ndb.Key('Message', pk)
        msg = key.get()
        self.assertEqual(msg, None)
        self.assertEqual(Message.query().count(), count - 1)

    def test_put_message(self):
        msg = self.add_message()
        count = Message.query().count()
        url = '/api/messages/%s/' % msg.message_id
        response = self.app.put(url, data=self.put,
                                follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        load = json.loads(response.data)
        self.assertEqual(load['message_id'], self.put['message_id'])
        self.assertEqual(load['message_data'], self.put['message_data'])
        self.assertIn('created_on', load)
        # nothing should change
        self.assertEqual(Message.query().count(), count)

    def test_message_list(self):
        url = '/admin/messages/'
        response = self.app.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
