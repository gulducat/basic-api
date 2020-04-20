from unittest import TestCase
from unittest.mock import Mock

from basic_api import BasicAPI
from basic_api.exceptions import NoAdapterError, NoMethodError


class TestBasicAPI(TestCase):
    cool_url = 'https://api.example.com/cool/path'

    def setUp(self):
        self.adapter = Mock()
        self.api = BasicAPI('api.example.com', adapter=self.adapter)

    def test_get(self):
        self.api.get()
        self.adapter.get.assert_called_once_with(url='https://api.example.com')

    def test_post(self):
        data = {'some': 'data'}
        self.api.post(data=data)
        self.adapter.post.assert_called_once_with(
            url='https://api.example.com', data=data)

    def test_get_path_arg(self):
        self.api.get('/cool/path')
        self.adapter.get.assert_called_once_with(url=self.cool_url)

    def test_get_attrs(self):
        self.api.get.cool.path()
        self.adapter.get.assert_called_once_with(url=self.cool_url)

    def test_get_items(self):
        self.api.get['cool']['path']()
        self.adapter.get.assert_called_once_with(url=self.cool_url)

    def test_get_item_with_slash(self):
        self.api.get['cool/path']()
        self.adapter.get.assert_called_once_with(url=self.cool_url)

    def test_get_mixed(self):
        self.api['get'].cool['path']()
        self.adapter.get.assert_called_once_with(url=self.cool_url)

    def test_multiple_calls(self):
        # make sure BasicAPI._clear() does its job
        self.api.get('/cool/path')
        self.adapter.reset_mock()
        self.api.get('/cool/path')
        self.adapter.get.assert_called_once_with(url=self.cool_url)

    def test_sequential_attrs(self):
        self.api.get
        self.api.cool["path"]
        self.api()
        self.adapter.get.assert_called_once_with(url=self.cool_url)

    def test_no_adapter(self):
        with self.assertRaises(NoAdapterError):
            BasicAPI('api.example.com', adapter=None)

    def test_no_method(self):
        with self.assertRaises(NoMethodError):
            self.api()

    def test_duplicate_kw(self):
        api = BasicAPI('api.example.com', headers=None, adapter=self.adapter)
        with self.assertRaises(TypeError):
            api.get(headers=None)
