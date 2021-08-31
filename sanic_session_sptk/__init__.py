# -*- coding: utf-8 -*-
#
from sanic_session.memcache import MemcacheSessionInterface
from sanic_session.redis import RedisSessionInterface
from sanic_session.memory import InMemorySessionInterface
from sanic_session.mongodb import MongoDBSessionInterface
from sanic_session.aioredis import AIORedisSessionInterface

from sanic_session_sptk.plugin import Session, session

__all__ = ('MemcacheSessionInterface', 'RedisSessionInterface',
           'InMemorySessionInterface', 'MongoDBSessionInterface',
           'AIORedisSessionInterface', 'Session', 'session')

__version__ = '0.6.0'
