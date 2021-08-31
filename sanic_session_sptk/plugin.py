# -*- coding: utf-8 -*-
#
import logging

from sanic_plugin_toolkit import SanicPlugin
from sanic_session import Session as RealSanicSession, InMemorySessionInterface


class Session(SanicPlugin):
    __slots__ = tuple()

    def __init__(self, *args, **kwargs):
        super(Session, self).__init__(*args, **kwargs)

    @classmethod
    def on_registered(cls, context, reg, *args, **kwargs):
        # this will need to be called more than once,
        # for every app it is registered on.
        app = context.app
        cls.init_app(app, context, *args, **kwargs)

    @classmethod
    def init_app(cls, app, context, *args, interface=None, **kwargs):
        log = context.log
        if interface is None:
            interface = InMemorySessionInterface()
        context.interface = interface
        real_session = RealSanicSession()
        real_session.interface = interface
        # Emulate old sanic-session method of attaching to app
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        # session_name defaults to 'session'
        app.extensions[interface.session_name] = real_session
        log(logging.DEBUG, "Created Session named: {} on app."
            .format(interface.session_name))


instance = session = Session()


@session.middleware(attach_to="request", with_context=True)
async def add_session_to_request_context(request, context):
    interface = context.interface
    shared_context = context.shared
    shared_request_context = shared_context.request[id(request)]
    dummy_request = shared_request_context.create_child_context()
    dummy_request.cookies = request.cookies
    session_dict = await interface.open(dummy_request)
    shared_request_context[interface.session_name] = session_dict


@session.middleware(attach_to="response", with_context=True)
async def save_session(request, response, context):
    interface = context.interface
    try:
        shared_request_context = context.shared.request[id(request)]
    except (AttributeError, KeyError) as e:
        # It is possible for RESPONSE middleware to run on a 404 error _before_
        # the request middleware has run. So in this case, there is no session.
        s = int(getattr(response, 'status', 200))
        if 400 <= s <= 499:
            return
        raise
    # We dont need a dummy request or response here
    await interface.save(shared_request_context, response)
