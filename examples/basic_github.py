import os

from basic_api import BasicAPI


class GitHub(BasicAPI):
    def __init__(self, token=None):
        """Basic GitHub API client.
        https://developer.github.com/v3/
        """
        super().__init__(host='api.github.com')
        token = os.environ.get('GITHUB_TOKEN', token)
        if token:
            self._adapter_kw['headers'] = {
                'Authorization': 'token ' + token
            }

    def __call__(self, path='', **adapter_kw):
        resp = super().__call__(path=path, **adapter_kw)
        resp.raise_for_status()
        return resp.json()
