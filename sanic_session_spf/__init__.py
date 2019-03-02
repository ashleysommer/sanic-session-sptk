# -*- coding: utf-8 -*-
#
from sanic_session.memcache import MemcacheSessionInterface
from sanic_session.redis import RedisSessionInterface
from sanic_session.memory import InMemorySessionInterface
from sanic_session.mongodb import MongoDBSessionInterface
from sanic_session.aioredis import AIORedisSessionInterface
from sanic_session.base import BaseSessionInterface

from sanic_session_spf.plugin import Session, session

__all__ = ('MemcacheSessionInterface', 'RedisSessionInterface',
           'InMemorySessionInterface', 'MongoDBSessionInterface',
           'AIORedisSessionInterface', 'Session')

class Session:

    def __init__(self, app=None, interface=None):
        if app:
            self.init_app(app, interface=interface)

    def init_app(self, app, interface=None):
        if interface is None:
            interface = InMemorySessionInterface()

        self.interface = interface
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions[interface.session_name] = self  # session_name defaults to 'session'

        # @app.middleware('request')
        async def add_session_to_request(request):
            """Before each request initialize a session
            using the client's request."""
            await self.interface.open(request)

        # @app.middleware('response')
        async def save_session(request, response):
            """After each request save the session, pass
            the response to set client cookies.
            """
            await self.interface.save(request, response)

        app.request_middleware.appendleft(add_session_to_request)
        app.response_middleware.append(save_session)