from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import fields, widgets

COLOR_CHOICES = [
    ('modifier', 'Color by modifier'),
    ('category', 'Color by category'),
    ('none', 'No colors'),
]
CATEGORY_CHOICES = [
    ('ship', 'Ship'),
    ('srv', 'SRV'),
    ('scanners', 'Scanners'),
    ('fighter', 'Fighter'),
    ('onfoot', 'On Foot'),
    ('multicrew', 'Multicrew'),
    ('headlook', 'Head Look'),
    ('ui', 'UI'),
    ('galaxymap', 'Galaxy Map'),
    ('camera', 'Camera'),
    ('holome', 'Holo-Me'),
    ('misc', 'Miscellaneous'),
]
FILE_DESCRIPTION = ("On Windows, the bindings are located on "
                    "%LOCALAPPDATA%\\Frontier Developments\\Elite Dangerous\\Options\\Bindings")
DESCRIPTION_DESCRIPTION = 'If you want to publish your bindings, give them a description here'


class MultiCheckboxField(fields.SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class BindingCreate(FlaskForm):
    binds_file = fields.FileField('Bindings file', [FileRequired(), FileAllowed(['binds'])],
                                  description=FILE_DESCRIPTION, render_kw={'accept': '.binds'})
    description = fields.StringField('Public description', description=DESCRIPTION_DESCRIPTION)
    categories = MultiCheckboxField('Categories', choices=CATEGORY_CHOICES)
    color_by = fields.RadioField('Color options', choices=COLOR_CHOICES, default='none')
    generate = fields.SubmitField('Generate reference card')
