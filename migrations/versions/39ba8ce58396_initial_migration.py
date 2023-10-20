"""Initial migration

Revision ID: 39ba8ce58396
Revises: 
Create Date: 2023-10-20 22:46:10.074880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39ba8ce58396'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('binding',
    sa.Column('raw_file', sa.String(), nullable=False),
    sa.Column('label', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('categories', sa.JSON(), nullable=True),
    sa.Column('color_by', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('label')
    )
    op.create_table('command',
    sa.Column('label', sa.String(), nullable=False),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('overridden_by', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('label')
    )
    op.create_table('device',
    sa.Column('label', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('filename', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('label')
    )
    op.create_table('key_map',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('modifies_id', sa.String(), nullable=True),
    sa.Column('index', sa.Integer(), nullable=False),
    sa.Column('device', sa.String(), nullable=False),
    sa.Column('key', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['modifies_id'], ['binding.label'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('binding_command',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('binding_id', sa.String(), nullable=False),
    sa.Column('command_id', sa.String(), nullable=False),
    sa.Column('mapping_id', sa.Integer(), nullable=False),
    sa.Column('modifiers', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['binding_id'], ['binding.label'], ),
    sa.ForeignKeyConstraint(['command_id'], ['command.label'], ),
    sa.ForeignKeyConstraint(['mapping_id'], ['key_map.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('binding_command')
    op.drop_table('key_map')
    op.drop_table('device')
    op.drop_table('command')
    op.drop_table('binding')
    # ### end Alembic commands ###
