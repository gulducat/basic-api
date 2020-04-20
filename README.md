# Basic API Client

`BasicAPI` is a Python API client that knows nothing about any specific APIs.

It's intended to be extended by subclasses which may have varying degrees
of knowledge of their target API, including auth and/or convenience methods.

Requires Python 3.5+ even though it would be easy to support lower versions.
Please use modern Python!

## Usage

```
pip install requests basic-api
```

```python
from basic_api import BasicAPI
api = BasicAPI('example.com')
```

All of the below are equivalent.
They make a GET request to `https://example.com/cool/path`

```python
api.get('/cool/path')
api.get.cool.path()
api.get['cool']['path']()
api.get['cool/path']()
api['get'].cool['path']()
```

The `[item]` syntax is useful for variables, and paths that include `.`s.

Example POST request:

```python
api.post('/cool/path', json={'some': 'data'})
```

This also works the same as the above, by happenstance:

```python
api.post
api.cool['path']
api(json={'some': 'data'})
```

See `Heads Up -> Thread Safety` below.

### Request adapter

The default adapter is [`requests`](https://requests.readthedocs.io/).
It is not a hard requirement for folks who wish to keep requirements to the bare minimum.


There is no fallback default adapter, so either install `requests`
or `basic-api[adapter]` or pass in some specific adapter.

All keyword arguments aside from `host`, `proto`, and `adapter`
will be passed into the adapter call.

For example, you may wish to include the same header on all API calls:

```python
api = BasicAPI('example.com', headers={'User-Agent': 'my fancy app'})
```

Note that if you try to include the same keyword in subsequent calls,
an exception will be raised:

```python
> api.get('/cool/path', headers={'another': 'header'})
TypeError: get() got multiple values for keyword argument 'headers'
```

Any attempt by `BasicAPI` to guess what you meant would make it not-so-basic,
so there are no current plans to change this behavior.

#### Sessions

For APIs (or API-like things) that support it, you may pass in a
[`requests.Session()`](https://2.python-requests.org/en/master/user/advanced/#session-objects)
as the `adapter`, since it has (mostly) the same interface as `requests` itself.

```python
sesh = requests.Session()
sesh.headers = {'User-Agent': 'my fancy app'}
# sesh.get(something something cookies)
api = BasicAPI('example.com', adapter=sesh)
```

#### Advanced

The `adapter` can be any instantiated object.

If you're advanced, you can probably figure out how to do fancy stuff with this basic thing.

## Heads Up

### Thread Safety

BasicAPI is _not_ thread safe (it is a BasicAPI, after all).

Instantiate one per thread if you are multithreading.
