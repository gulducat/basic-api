import logging
from copy import deepcopy

from . import exceptions as exc

logger = logging.getLogger(__name__)

try:
    import requests
    ADAPTER = requests
except ImportError:
    logger.info('no "requests" package found, so no default adapter')
    ADAPTER = None


class BasicAPI:
    def __init__(self, host, proto='https://', adapter=ADAPTER, **adapter_kw):
        """Make API requests as naively as possible.
        See https://github.com/gulducat/basic-api/ for readme.

        :param host: hostname
        :param proto: protocol, default "https://"
        :param adapter: object that makes the api call (default requests)
        :param **adapter_kw: keyword arguments to include in calls
        :raises NoAdapterError: if no "requests", and no adapter provided.
        """
        self._base_url = proto + host
        if not adapter:
            raise exc.NoAdapterError('no "requests", and no adapter provided')
        self._adapter = adapter
        self._adapter_kw = adapter_kw
        self._prepare()

        # this is what makes causes thread danger.
        self._paths = []
        self._method = None

    def _clear(self):
        """Reset per-call attributes."""
        self._paths = []
        self._method = None

    def _prepare(self):
        """Make any changes needed for calls to succeeed."""

    def __getattr__(self, attr):
        """Build the method + API path."""
        if self._method:
            self._paths.append(attr)
        else:
            # get/post/put/delete/head for "requests" adapter
            self._method = attr.lower()
        return self

    __getitem__ = __getattr__

    def __call__(self, path='', **adapter_kw):
        """Make API call.

        :param path: path to hit (default "")
        :param **adapter_kw: keyword arguments to include in the call
        :raises NoMethodError: if no HTTP method has been detected
        """
        if not self._method:
            raise exc.NoMethodError('no method provided, expecting ex: get')

        url = '/'.join([
            p.strip('/')
            for p in [self._base_url] + self._paths
        ]) + path
        method = self._method
        self._clear()

        if self._adapter_kw:
            kw = deepcopy(self._adapter_kw)
            merge(source=adapter_kw, dest=kw)
        else:
            kw = adapter_kw

        logger.debug('adapter kw: %s' % kw)
        return getattr(self._adapter, method)(url=url, **kw)


# there are a hundred million ways to skin this cat
# https://stackoverflow.com/questions/7204805/how-to-merge-dictionaries-of-dictionaries
# but the below merge function is pretty "basic" for our purposes.


def merge(source, dest):
    """Recursively merge a "source" dict into an "update" dict.
    :param source: authoritative dict
    :param dest: dict to dest, it will be mutated
    :returns dict: only really needed for recursion
    """
    logger.debug('merging %s -> %s' % (source, dest))
    if not isinstance(source, dict):
        return source
    for k, v in source.items():
        if isinstance(source, dict) and isinstance(dest, dict):
            dest[k] = merge(v, dest.get(k, {}))
        else:
            # sanity check, this basic thing can't do tooooo-fancy stuff
            # if anyone actually uses this, issues incoming?
            raise TypeError('cant merge non-dicts %s -> %s' % (source, dest))
    return dest
