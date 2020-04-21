from unittest import TestCase

from mock import Mock

from basic_api import BasicAPI, merge
from basic_api.exceptions import NoAdapterError, NoMethodError


class TestBasicAPI(TestCase):
    host = 'api.example.com'
    base_url = 'https://' + host
    cool_url = base_url + '/cool/path'

    def setUp(self):
        self.adapter = Mock()
        self.api = BasicAPI(self.host, adapter=self.adapter)

    def test_get(self):
        self.api.get()
        self.adapter.get.assert_called_once_with(url=self.base_url)

    def test_post(self):
        data = {'some': 'data'}
        self.api.post(data=data)
        self.adapter.post.assert_called_once_with(url=self.base_url, data=data)

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
        self.api.cool['path']
        self.api()
        self.adapter.get.assert_called_once_with(url=self.cool_url)

    def test_duplicate_kw_merge(self):
        api = BasicAPI(self.host, adapter=self.adapter,
                       headers={'ua': 'cool app'})
        api.get(another='kwarg')
        expected = {
            'headers': {'ua': 'cool app'},
            'another': 'kwarg',
        }
        self.adapter.get.assert_called_once_with(url=self.base_url, **expected)

    def test_duplicate_kw_override(self):
        cool = {'headers': {'ua': 'cool app'}}
        cooler = {'headers': {'ua': 'COOLER app'}}
        api = BasicAPI(self.host, adapter=self.adapter, **cool)

        api.get(**cooler)
        self.adapter.get.assert_called_once_with(url=self.base_url, **cooler)

        # ensure that api._adapter_kw is not mutated by merge.
        self.adapter.reset_mock()
        api.get()
        self.adapter.get.assert_called_once_with(url=self.base_url, **cool)

    def test_no_adapter(self):
        with self.assertRaises(NoAdapterError):
            BasicAPI(self.host, adapter=None)

    def test_no_method(self):
        with self.assertRaises(NoMethodError):
            self.api()


class TestDictMerge(TestCase):
    # testing recursive functions is funky.
    # gosh i probably shouldn't even be doing this.

    def test_simple_overwite(self):
        src = {'key': 'val1'}
        dest = {'key': 'val2'}
        expected = src.copy()
        merge(src, dest)
        self.assertEqual(expected, dest)

    def test_nested_overwite(self):
        src = {'key': {'sub': 'val1'}}
        dest = {'key': {'sub': 'val2'}}
        expected = src.copy()
        merge(src, dest)
        self.assertEqual(expected, dest)

    def test_diff_types(self):
        src = {'key': False}
        dest = {'key': 'hmmm'}
        expected = src.copy()
        merge(src, dest)
        self.assertEqual(expected, dest)

    def test_different_diff_source_type(self):
        src = 'ok'
        dest = {'key': False}
        expected = dest
        merge(src, dest)
        self.assertEqual(expected, dest)

    def test_different_diff_dest_type(self):
        src = {'key': False}
        dest = 'ok'
        with self.assertRaises(TypeError):
            merge(src, dest)

    def test_nested_merge(self):
        src = {'key': {'sub1': 'val1'}}
        dest = {'key': {'sub2': 'val2'}}
        expected = {'key': {'sub1': 'val1', 'sub2': 'val2'}}
        merge(src, dest)
        self.assertEqual(expected, dest)
