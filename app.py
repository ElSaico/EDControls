from operator import attrgetter

from itertools import groupby

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_migrate import Migrate
from flask_talisman import Talisman
from lxml import etree
from sqlalchemy import func

import forms
from models import *

app = Flask(__name__)
app.secret_key = 'o7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bindings.db'
bootstrap = Bootstrap5(app)
Talisman(app, content_security_policy={
    'style-src': ["'self'", 'cdn.jsdelivr.net'],
    'script-src': ["'self'", 'cdn.jsdelivr.net'],
})
db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def home():
    return render_template("index.html", form=forms.BindingCreate())


@app.post("/bindings")
def upload_bindings():
    form = forms.BindingCreate()
    if form.validate_on_submit():
        binds = Binding(
            raw_file=form.binds_file.data.read(),
            description=form.description.data,
            color_by=form.color_by.data,
            categories=form.categories.data,
        )
        db.session.add(binds)
        root = etree.fromstring(binds.raw_file)
        for element in root.findall(".//Binding") + root.findall(".//Primary") + root.findall(".//Secondary"):
            command_name = element.getparent().tag
            command = db.session.get(Command, command_name)
            if not command:
                app.logger.warning('Unregistered command: %s', command_name)
                continue
            if command.category not in binds.categories:
                continue
            if element.get('Device') in ['{NoDevice}', 'Mouse']:
                continue
            if element.get('Device') == 'Keyboard':
                modifiers = [modifier.get('Key') for modifier in element.xpath('./Modifier')]
            else:
                modifiers = []
                for modifier in element.xpath('./Modifier'):
                    device = modifier.get('Device')
                    key = modifier.get('Key')
                    index_query = db.select(Modifier.index).filter_by(binding_id=binds.label, device=device, key=key)
                    index = db.session.execute(index_query).scalar()
                    if not index:
                        modifier = Modifier(device=device, key=key)
                        binds.modifiers.append(modifier)
                        index = modifier.index
                    modifiers.append(index)
            binding_command = BindingCommand(
                binding_id=binds.label,
                command_id=command_name,
                device=element.get('Device'),
                key=element.get('Key'),
                modifiers=modifiers,
            )
            db.session.add(binding_command)
        db.session.commit()
        return redirect(url_for('render_bindings', label=binds.label))
    # TODO redirect to index showing errors


@app.get("/bindings")
def list_bindings():
    ...


@app.get("/bindings/<label>")
def render_bindings(label):
    binds = db.get_or_404(Binding, label)
    controllers_query = (
        db.select(Device.template_id, BindingCommand.key,
                  func.json_group_object(BindingCommand.command_id, func.json(BindingCommand.modifiers)).label('commands'))
        .join_from(Device, BindingCommand, BindingCommand.device == Device.label)
        .where(BindingCommand.binding_id == label, BindingCommand.device != 'Keyboard')
        .group_by(BindingCommand.device, BindingCommand.key)
    )
    controllers = db.session.execute(controllers_query).all()
    controllers = {template: list(keys) for template, keys in groupby(controllers, attrgetter('template_id'))}
    keyboard_query = (
        db.select(
            Command.category, func.json_group_object(
                Command.name, func.json_insert(BindingCommand.modifiers, '$[#]', BindingCommand.key)).label('commands')
        ).join_from(Command, BindingCommand)
        .where(BindingCommand.binding_id == label, BindingCommand.device == 'Keyboard')
        .group_by(Command.category)
        .order_by(Command.order)
    )
    keyboard = db.session.execute(keyboard_query).all()
    return render_template("binds.html", binds=binds, controllers=controllers, keyboard=keyboard)


@app.route("/devices")
def list_devices():
    ...
