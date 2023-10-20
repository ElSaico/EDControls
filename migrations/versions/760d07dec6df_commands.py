"""Commands

Revision ID: 760d07dec6df
Revises: 39ba8ce58396
Create Date: 2023-10-20 16:21:08.528047

"""
import json
from pathlib import Path

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '760d07dec6df'
down_revision = '39ba8ce58396'
branch_labels = None
depends_on = None

commands_table = sa.table(
    'command',
    sa.column('label', sa.String),
    sa.column('category', sa.String),
    sa.column('order', sa.Integer),
    sa.column('name', sa.String),
    sa.column('overridden_by', sa.String),
)


def upgrade():
    with open(Path(__file__).parent / '../commands.json') as f:
        commands = json.load(f)
    op.bulk_insert(commands_table, commands)


def downgrade():
    pass
