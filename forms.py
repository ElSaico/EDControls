from flask_wtf import FlaskForm
from wtforms import fields, validators

COLOR_CHOICES = [
    ('modifier', 'Color by modifier'),
    ('category', 'Color by category'),
    ('none', 'No colors'),
]


class BindingCreate(FlaskForm):
    binds_file = fields.FileField('Bindings file', [validators.input_required()])
    description = fields.StringField('Public description')
    color_by = fields.RadioField('Color options', choices=COLOR_CHOICES)
    generate = fields.SubmitField('Generate reference card')
