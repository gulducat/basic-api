import logging

from . import exceptions as exc

logger = logging.getLogger(__name__)

try:
    import requests
    ADAPTER = requests
except ImportError:
    logger.warning('no "requests" package found, so no default adapter')
    ADAPTER = None


class BasicAPI:
    def __init__(self, host, proto="https://", adapter=ADAPTER, **adapter_kw):
        """Make API requests as ignorantly as possible.
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
        pass

    def __getattr__(self, attr):
        """Build the method + API path."""
        if self._method:
            self._paths.append(attr)
        else:
            # get/post/put/delete/head for "requests" adapter
            self._method = attr.lower()
        return self

    __getitem__ = __getattr__

    def __call__(self, path="", **adapter_kw):
        """Make API call.

        :param path: path to hit (default "")
        :param **adapter_kw: keyword arguments to include in the call
        :raises NoMethodError: if no HTTP method has been detected
        :raises TypeError: if multiple of the same keyword arguments collide
        """
        if not self._method:
            raise exc.NoMethodError('no method provided, expecting ex: get')

        url = '/'.join([
            p.strip('/')
            for p in [self._base_url] + self._paths
        ]) + path
        method = self._method
        self._clear()

        # double **kw is not available in py2 or py3<3.5 (SyntaxError)
        # leaving it like on purpose.
        return getattr(self._adapter, method)(
            url=url, **adapter_kw, **self._adapter_kw)
