try:
    from unittest.mock import Mock
    from unittest.mock import patch
except ImportError:
    from mock import Mock
    from mock import patch

from moira_client.client import Client
from moira_client.client import InvalidJSONError
from moira_client.client import ResponseStructureError
from moira_client.models.tag import TagManager
from .test_model import ModelTest


class TagTest(ModelTest):

    def test_fetch_all(self):
        client = Client(self.api_url)
        tag_manager = TagManager(client)

        with patch.object(client, 'get', return_value={'list': []}) as get_mock:
            tag_manager.fetch_all()

        self.assertTrue(get_mock.called)
        get_mock.assert_called_with('tag/')

    def test_fetch_all_bad_response(self):
        client = Client(self.api_url)
        tag_manager = TagManager(client)

        with patch.object(client, 'get', return_value={}) as get_mock:
            with self.assertRaises(ResponseStructureError):
                tag_manager.fetch_all()

        self.assertTrue(get_mock.called)
        get_mock.assert_called_with('tag/')

    def test_delete(self):
        client = Client(self.api_url)
        tag_manager = TagManager(client)

        tag = 'tag'

        with patch.object(client, 'delete') as delete_mock:
            res = tag_manager.delete(tag)

        self.assertTrue(delete_mock.called)
        self.assertTrue(res)
        delete_mock.assert_called_with('tag/' + tag)

    def test_delete_fail(self):
        client = Client(self.api_url)
        tag_manager = TagManager(client)

        tag = 'tag'

        with patch.object(client, 'delete', new=Mock(side_effect=InvalidJSONError(b''))) as delete_mock:
            res = tag_manager.delete(tag)

        self.assertTrue(delete_mock.called)
        self.assertFalse(res)
        delete_mock.assert_called_with('tag/' + tag)

    def test_stats(self):
        client = Client(self.api_url)
        tag_manager = TagManager(client)
        extra_data = {
            'key': 'value'
        }
        tag_name = 'tag_name'
        subscription_id = '3c01399e-1d40-46dd-934f-318e8255fd3e'
        return_value = {
            'list': [
                {
                    'data': extra_data,
                    'name': tag_name,
                    'subscriptions': [
                        {
                            'contacts': ['3c01399e-1d40-46dd-934f-318e8255fd3e'],
                            'enabled': True,
                            'id': subscription_id,
                            'days': [
                                {'name': 'Mon', 'enabled': True},
                                {'name': 'Tue', 'enabled': True},
                                {'name': 'Wed', 'enabled': True},
                                {'name': 'Thu', 'enabled': True},
                                {'name': 'Fri', 'enabled': True},
                                {'name': 'Sat', 'enabled': True},
                                {'name': 'Sun', 'enabled': True}
                            ],
                            'endOffset': 1439,
                            'startOffset': 0,
                            'tzOffset': -180
                        }
                    ],
                    'triggers': []
                }
            ]
        }

        with patch.object(client, 'get', return_value=return_value) as get_mock:
            stats = tag_manager.stats()

            self.assertTrue(get_mock.called)
            self.assertEqual(1, len(stats))
            self.assertEqual(extra_data, stats[0].data)
            self.assertEqual(tag_name, stats[0].name)
            self.assertEqual(1, len(stats[0].subscriptions))
            self.assertEqual(subscription_id, stats[0].subscriptions[0].id)

    def test_add_data(self):
        client = Client(self.api_url)
        tag_manager = TagManager(client)
        tag_name = 'tag_name'
        data = {
            'key': 'value'
        }

        with patch.object(client, 'put', side_effect=ResponseStructureError('', b'')) as get_mock:
            result = tag_manager.add_data(tag_name, data)

            self.assertTrue(get_mock.called)
            self.assertTrue(result)

    def test_fetch_assigned_triggers(self):
        client = Client(self.api_url)
        tag_manager = TagManager(client)

        extra_data = {
            'key': 'value'
        }
        tag_name = 'tag_name'
        subscription_id = '3c01399e-1d40-46dd-934f-318e8255fd3e'
        trigger_id = '123'
        return_value = {
            'list': [
                {
                    'data': extra_data,
                    'name': tag_name,
                    'subscriptions': [
                        {
                            'contacts': ['1'],
                            'enabled': True,
                            'id': subscription_id,
                            'days': [
                                {'name': 'Mon', 'enabled': True},
                                {'name': 'Tue', 'enabled': True},
                                {'name': 'Wed', 'enabled': True},
                                {'name': 'Thu', 'enabled': True},
                                {'name': 'Fri', 'enabled': True},
                                {'name': 'Sat', 'enabled': True},
                                {'name': 'Sun', 'enabled': True}
                            ],
                            'endOffset': 1439,
                            'startOffset': 0,
                            'tzOffset': -180
                        }
                    ],
                    'triggers': [trigger_id]
                }
            ]
        }

        with patch.object(client, 'get', return_value=return_value) as get_mock:
            triggers = tag_manager.fetch_assigned_triggers(tag_name)

            self.assertTrue(get_mock.called)
            get_mock.assert_called_with('trigger/')
            self.assertEqual(1, len(triggers))

    def test_fetch_assigned_subscriptions(self):
        client = Client(self.api_url)
        tag_manager = TagManager(client)

        extra_data = {
            'key': 'value'
        }
        tag_name = 'tag_name'
        subscription_id = '3c01399e-1d40-46dd-934f-318e8255fd3e'
        trigger_id = '123'
        return_value = {
            'list': [
                {
                    'data': extra_data,
                    'name': tag_name,
                    'subscriptions': [
                        {
                            'contacts': ['1'],
                            'enabled': True,
                            'id': subscription_id,
                            'days': [
                                {'name': 'Mon', 'enabled': True},
                                {'name': 'Tue', 'enabled': True},
                                {'name': 'Wed', 'enabled': True},
                                {'name': 'Thu', 'enabled': True},
                                {'name': 'Fri', 'enabled': True},
                                {'name': 'Sat', 'enabled': True},
                                {'name': 'Sun', 'enabled': True}
                            ],
                            'endOffset': 1439,
                            'startOffset': 0,
                            'tzOffset': -180
                        }
                    ],
                    'triggers': [trigger_id]
                }
            ]
        }

        with patch.object(client, 'get', return_value=return_value) as get_mock:
            subscriptions = tag_manager.fetch_assigned_subscriptions(tag_name)

            self.assertTrue(get_mock.called)
            get_mock.assert_called_with('tag/stats')
            self.assertEqual(1, len(subscriptions))
            self.assertEqual(subscription_id, subscriptions[0].id)
