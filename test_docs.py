#!/usr/bin/env python

"""
probably shouldn't be doing this, but rolling my own
super basic doctest helps keep docstrings and readme clean.
it's quite fragile, but i'm ok with that.
"""

import re

import requests  # noqa
import requests_mock


def test_docs(requests_mock):
    # requests_mock makes sure only this url gets hit.
    url = 'https://api.example.com/cool/path'
    requests_mock.get(url, text='ok')
    requests_mock.post(url, text='ok')

    with open('README.md') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if ' = ' in line or line.startswith('from '):
            print('>>> ' + line)
            exec(line)
            continue

        if not line.startswith('api'):
            continue

        if not line.endswith(')'):
            print('>>> ' + line)
            exec(line)
            continue

        print('>>> resp = ' + line)
        resp = eval(line)
        assert resp.text == 'ok'

        # the below is kinda complicated, and not strictly necessary
        # since the logic is tested elsewhere, but eh, i wrote it
        # so here it remains.

        request_kw = re.search(r'(\w+)=(\{.*\})', line)
        if not request_kw:
            continue

        kw, val = request_kw.groups()
        print("#", kw, val)
        val = eval(val)

        if kw == 'json':
            json = eval('resp.request.json()')
            assert json == val

        elif kw == 'headers':
            headers = eval('resp.request.headers')
            intersection = {}
            for k, v in val.items():
                if headers[k] == v:
                    intersection[k] = v
            assert intersection == val


if __name__ == '__main__':
    with requests_mock.Mocker() as m:
        test_docs(m)
