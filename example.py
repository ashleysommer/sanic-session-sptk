from uuid import uuid4
from sanic import Sanic
from sanic.response import text
from spf import SanicPluginsFramework
from sanic_session_spf.plugin import session
from spf.plugins import contextualize

app = Sanic(__name__)
spf = SanicPluginsFramework(app)
session_reg = spf.register_plugin(session, interface=None)
ctx = spf.register_plugin(contextualize)

@ctx.route("/")
def index(request, context):
    session = context.shared.session
    token = session.get("RememberMe", None)
    if token is None:
        session['RememberMe'] = token = str(uuid4())
    return text(token)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="9998", debug=True, auto_reload=False)