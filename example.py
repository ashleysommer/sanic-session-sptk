from uuid import uuid4
from sanic import Sanic
from sanic.response import text
from sanic_plugin_toolkit import SanicPluginRealm
from sanic_session_sptk.plugin import session
from sanic_plugin_toolkit.plugins import contextualize

app = Sanic(__name__)
sptk = SanicPluginRealm(app)
session_reg = sptk.register_plugin(session, interface=None)
ctx = sptk.register_plugin(contextualize)

@ctx.route("/")
def index(request, context):
    session = context.shared.request[id(request)].session
    token = session.get("RememberMe", None)
    if token is None:
        session['RememberMe'] = token = str(uuid4())
    return text("{} {}".format(id(request), token))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="9997", debug=True, auto_reload=False)
