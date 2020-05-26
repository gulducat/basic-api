# Basic API Client

`BasicAPI` is a Python API client that knows nothing about any specific APIs.

## Purpose

I've used a lot of complicated python clients that are of course useuful,
but my favorite clients are very basic.  They're _so not-smart_ that the question
"Is this a problem with the API, or a problem with the python client?"
should be more on the API than the client.

So, `BasicAPI` is very slim.  After a bit of understanding of how it works,
generally you should read the API docs instead of client docs.

It's intended to be extended by subclasses which may have varying degrees
of knowledge of their target API, including auth and/or convenience methods.

### Example

An example subclass can be found in
[`examples/basic_github.py`](https://github.com/gulducat/basic-api/blob/master/examples/basic_github.py)
which is used for cutting releases of `basic-api` in
[`release.py`](https://github.com/gulducat/basic-api/blob/master/release.py).

## Usage

```
pip install requests basic-api
```

```python
from basic_api import BasicAPI
api = BasicAPI('https://api.example.com')
```

All of the below are equivalent.
They make a GET request to `https://api.example.com/cool/path`

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
It is not a hard requirement for folks who wish to keep requirements to the bare minimum,
but there is no fallback adapter, so either install `requests`
or `basic-api[adapter]` (which includes requests) or pass in some specific adapter.

All keyword arguments aside from `base_url` and `adapter`
will be passed into the adapter call.

For example, you may wish to include the same header on all API calls:

```python
api = BasicAPI('https://api.example.com', headers={'User-Agent': 'fancy'})
```

#### Overlapping kwargs

If you include the same keyword in subsequent calls,
`BasicAPI` will do a not-so-basic thing and attempt to merge them together,
preferring the value(s) in the API call, so with

```python
api = BasicAPI('https://api.example.com', headers={'User-Agent': 'fancy'})
api.get('/cool/path', headers={'User-Agent': 'super fancy'})
```

the `get` call will override the previous `User-Agent` header,
resulting in a "super fancy" user agent, and

```python
api.get('/cool/path', headers={'another': 'header'})
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
api = BasicAPI('https://api.example.com', adapter=sesh)
# api.post.something.something.cookies()
api.post('/cool/path')
```

#### Advanced

The `adapter` can be any object with callable attributes.

If you are advanced, you can probably figure out how to do exceptional stuff with this basic thing.

## Heads Up

### Thread Safety

BasicAPI is _not_ thread safe (it is quite basic, after all).

Instantiate one per thread if you are multithreading.
They don't cost much.
