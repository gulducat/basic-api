#!/usr/bin/env python

from argparse import ArgumentParser

from basic_github import GitHub
from setup import VERSION


def parse_args():
    parser = ArgumentParser(description='Create a Draft release in GitHub')
    parser.add_argument(
        '-t', '--token',
        help='API token (env GITHUB_TOKEN) with repo:public_repo access')
    return parser.parse_args()


def main(args):
    version = 'v' + VERSION
    gh = GitHub(token=args.token)

    # https://developer.github.com/v3/repos/releases/
    slug = 'gulducat/basic-api/releases'

    released = [
        r['name']
        for r in gh.get.repos[slug]().json()
    ]
    if version in released:
        print(version + ' already exists')
        return

    draft = gh.post.repos[slug](json=dict(
        tag_name=version,
        name=version,
        body='💃',
        draft=True,
    )).json()
    tag = draft['html_url'].split('/')[-1]
    url = 'https://github.com/%s/edit/%s' % (slug, tag)
    print('Draft release: ' + url)


if __name__ == '__main__':
    main(parse_args())
