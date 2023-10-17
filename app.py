from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_talisman import Talisman

import forms

app = Flask(__name__)
app.secret_key = 'o7'
bootstrap = Bootstrap5(app)
Talisman(app, content_security_policy={
    'style-src': ["'self'", 'cdn.jsdelivr.net'],
    'script-src': ["'self'", 'cdn.jsdelivr.net'],
})


@app.route("/")
def index():
    return render_template("index.html", form=forms.BindingCreate())


@app.route("/bindings")
def list_bindings():
    ...


@app.route("/devices")
def list_devices():
    ...
