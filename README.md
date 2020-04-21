# Basic API Client

`BasicAPI` is a Python API client that knows nothing about any specific APIs.

It's intended to be extended by subclasses which may have varying degrees
of knowledge of their target API, including auth and/or convenience methods.

An example can be found in `basic_github.py` which is used in `release.py`
for making releases of `basic-api`.

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

#### Overlapping kwargs

If you include the same keyword in subsequent calls,
`BasicAPI` will do a not-so-basic thing and attempt to merge them together,
preferring the value(s) in the API call, so with

```python
api = BasicAPI('example.com', headers={'User-Agent': 'fancy'})
api.get('/cool/path', headers={'User-Agent': 'super fancy'})
```

the `get` call will override the previous `User-Agent` header,
resulting in a "super fancy" user agent, and

```python
api.get('/cool/path', headers={'another', 'header'})
```

will result in both the original "fancy" user agent _and_ `another` header.

This behavior is sorta-tested; it's the only part of this thing I'm worried about.
It's probably fine, but no promises.  Your own integration tests
and `logging.basicConfig(level=logging.DEBUG)` are your friends.

Please tell me how wrong I am about my recursive `merge` function.

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
