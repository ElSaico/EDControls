from lxml import etree
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
def home():
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
        root = etree.fromstring(binds.raw_file)
        for element in root.findall(".//Binding") + root.findall(".//Primary") + root.findall(".//Secondary"):
            command_name = element.getparent().tag
            command = models.db.session.get(models.Command, command_name)
            if not command:
                app.logger.warning('Unregistered command: %s', command_name)
                continue
            if command.category not in binds.categories:
                continue
            if element.get('Device') == '{NoDevice}':
                continue
            if element.get('Device') == 'Keyboard':
                modifiers = [modifier.get('Key') for modifier in element.xpath('./Modifier')]
            else:
                modifiers = []
                for modifier in element.xpath('./Modifier'):
                    device = modifier.get('Device')
                    key = modifier.get('Key')
                    index = models.db.session.execute(
                        models.db.select(models.Modifier.index)
                        .filter_by(binding_id=binds.label, device=device, key=key)
                    ).scalar()
                    if not index:
                        modifier = models.Modifier(device=device, key=key)
                        binds.modifiers.append(modifier)
                        index = modifier.index
                    modifiers.append(index)
            binding_command = models.BindingCommand(
                binding_id=binds.label,
                command_id=command_name,
                device=element.get('Device'),
                key=element.get('Key'),
                modifiers=modifiers,
            )
            models.db.session.add(binding_command)
        models.db.session.commit()
        # TODO redirect to binding page
    # TODO redirect to index showing errors


@app.get("/bindings")
def list_bindings():
    ...


@app.route("/devices")
def list_devices():
    ...
