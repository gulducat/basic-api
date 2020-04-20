from setuptools import setup


def load_long_description():
    with open('README.md', 'r') as fh:
        return fh.read()


setup(
    name='basic-api',
    version='0.1.0',
    description='Basic API client',
    long_description=load_long_description(),
    long_description_content_type="text/markdown",
    author='Daniel Bennett',
    # author_email='',
    url='https://github.com/gulducat/basic-api',
    keywords=['basic', 'api', 'basic-api'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    packages=["basic_api"],
    include_package_data=True,
    package_data={'basic-api': ['version']},
    extras_require={
        # any version of requests should be fine
        'adapter': ['requests']
    }
)
