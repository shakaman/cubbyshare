import base64
import json
import os
import traceback
import uuid
import sys
import base64

import redis
import flask
import flask.json
from flask_bootstrap import Bootstrap

from .frontend import frontend
from .nav import nav


app = flask.Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = 'secretkey'
app.register_blueprint(frontend)
nav.init_app(app)

app.config['RELATIONSHIPS'] = json.loads(
    base64.b64decode(os.environ["PLATFORM_RELATIONSHIPS"])
)
app.redis = redis.StrictRedis(
    host=app.config['RELATIONSHIPS']['redis'][0]['host'], 
    port=app.config['RELATIONSHIPS']['redis'][0]['port'], 
    db=0
)
def get_token():
    return app.redis.get('token')
app.get_token = get_token


if __name__ == "__main__":
    # token = redis_conn.get('token')
    app.run(host='0.0.0.0', port=8888)