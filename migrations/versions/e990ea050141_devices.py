"""Devices

Revision ID: e990ea050141
Revises: 760d07dec6df
Create Date: 2023-10-22 17:46:10.109220

"""
import json
from pathlib import Path

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e990ea050141'
down_revision = '760d07dec6df'
branch_labels = None
depends_on = None

templates_table = sa.table(
    'device_template',
    sa.column('filename', sa.String),
    sa.column('name', sa.String),
)
devices_table = sa.table(
    'device',
    sa.column('label', sa.String),
    sa.column('template_id', sa.String),
)


def upgrade():
    with open(Path(__file__).parent / '../devices.json') as f:
        templates_raw = json.load(f)
    templates = [{'filename': template['template'], 'name': template['name']} for template in templates_raw]
    op.bulk_insert(templates_table, templates)
    for template in templates_raw:
        devices = [{'label': device, 'template_id': template['template']} for device in template['devices']]
        op.bulk_insert(devices_table, devices)


def downgrade():
    pass
