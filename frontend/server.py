import base64
import json
import os
import traceback
import uuid
import sys

import flask
import flask.json


app = flask.Flask(__name__)
relationships = json.loads(base64.b64decode(os.environ["PLATFORM_RELATIONSHIPS"]))


@app.route('/')
def root():
    tests = {}
    return flask.json.jsonify(tests)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888)
