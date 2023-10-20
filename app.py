from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_migrate import Migrate
from flask_talisman import Talisman

import forms
import models

app = Flask(__name__)
app.secret_key = 'o7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bindings.db'
bootstrap = Bootstrap5(app)
Talisman(app, content_security_policy={
    'style-src': ["'self'", 'cdn.jsdelivr.net'],
    'script-src': ["'self'", 'cdn.jsdelivr.net'],
})
models.db.init_app(app)
migrate = Migrate(app, models.db)


@app.route("/")
def index():
    return render_template("index.html", form=forms.BindingCreate())


@app.post("/bindings")
def upload_bindings():
    form = forms.BindingCreate()
    if form.validate_on_submit():
        binds = models.Binding(
            raw_file=form.binds_file.data.read(),
            description=form.description.data,
            color_by=form.color_by.data,
            categories=form.categories.data,
        )
        models.db.session.add(binds)
        # TODO XML processing and bla
        models.db.session.commit()


@app.get("/bindings")
def list_bindings():
    ...


@app.route("/devices")
def list_devices():
    ...
