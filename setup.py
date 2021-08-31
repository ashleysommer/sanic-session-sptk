# -*- coding: utf-8 -*-
#
import codecs

from setuptools import setup
import re
import os


def open_local(paths, mode='r', encoding='utf8'):
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        *paths
    )
    return codecs.open(path, mode, encoding)


with open_local(['sanic_session_sptk', '__init__.py'], encoding='utf-8') as fp:
    try:
        version = re.findall(r"^__version__ = '([^']+)'\r?$",
                             fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')

with open_local(['README.md']) as readme:
    long_description = readme.read()


with open_local(['requirements.txt']) as req:
    install_requires = req.read().split("\n")


setup(
    name='Sanic-Session-SPTK',
    version=version,
    url='https://github.com/ashleysommer/sanic-session-sptk',
    license='MIT',
    author='Ashley Sommer, Suby Raman',
    author_email='ashleysommer@gmail.com',
    description="A SPF compatible distribution of Sanic-Session. Wraps upstream Sanic-Session.",
    long_description=long_description,
    packages=['sanic_session_sptk'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=install_requires,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
