import os
import base64

import hvac
from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
    current_app,
    jsonify
)
from flask_nav.elements import Navbar, View

from .forms import DataForm
from .nav import nav


frontend = Blueprint("frontend", __name__)


nav.register_element(
    "frontend_top",
    Navbar(
        View("Cubbyshare", ".index"),
        View("Home", ".index"),
        View("About", ".about")
    ),
)


@frontend.route("/", defaults={"path": ""})
@frontend.route("/<path:path>")
def index(path):
    if not path:
        form = DataForm()
        return render_template("index.html", form=form, data="")
    if current_app.debug:
        result_url = url_for(
            '.get_data', path=path
        )
    else:
        result_url = url_for(
            '.get_data', path=path, _external=True, _scheme='https'
        )
    return render_template(
        "index.html",
        form="",
        result_url=result_url
    )


@frontend.route("/_get_data/<path:path>")
def get_data(path):
    token = path
    if not token:
        return redirect(url_for(".index"))

    if current_app.debug:
        secret = "123\n123"
    else:
        vault_uri = os.environ.get("VAULT_URI", None)
        if not vault_uri:
            flash("Missing VAULT_URI")
            return redirect(url_for(".index"))
        try:
            cubby = hvac.Client(url=vault_uri, token=token)
            result = cubby.read("cubbyhole/%s" % token)
        except hvac.exceptions.Forbidden:
            return jsonify(result="link expired")
        secret = base64.b64decode(result["data"]["wrap"]).decode()
    return jsonify(result=secret)


@frontend.route("/add", methods=["POST"])
def add_entry():
    form = DataForm()

    if form.validate_on_submit():
        secret_data = base64.b64encode(form.secrets.data.encode()).decode()
        root_token = current_app.get_token()

        if current_app.debug:
            token_id="0000"
        else:
            vault_uri = os.environ.get("VAULT_URI", None)
            if not vault_uri:
                flash("Missing VAULT_URI")
                return redirect(url_for(".index"))

            vault = hvac.Client(url=vault_uri, token=root_token)
            token = vault.create_token(
                lease="24h",
                num_uses=2,
                renewable=False,
                no_default_policy=True,
            )
            token_id = token["auth"]["client_token"]

            cubby = hvac.Client(url=vault_uri, token=token_id)
            cubby.write("cubbyhole/%s" % token_id, wrap=secret_data)
        flash("Successfully saved")

        return render_template("success.html", token=token_id)
    else:
        for error_field, error_message in form.errors.items():
            flash(
                "Field : {field}; error : {error}".format(
                    field=error_field, error=error_message
                )
            )

    return redirect(url_for(".index"))


@frontend.route("/about")
def about():
    return render_template("about.html")
