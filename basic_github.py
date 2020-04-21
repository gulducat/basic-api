import os

import requests
from basic_api import BasicAPI


class GitHub(BasicAPI):
    def __init__(self, token=None):
        """Basic GitHub API client.
        https://developer.github.com/v3/
        """
        self._token = os.environ.get('GITHUB_TOKEN', token)
        super().__init__(host='api.github.com', adapter=requests)

    def _prepare(self):
        if self._token:
            self._adapter_kw['headers'] = {
                'Authorization': 'token ' + self._token
            }
