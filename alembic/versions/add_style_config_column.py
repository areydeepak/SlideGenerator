"""add style_config column

Revision ID: add_style_config_column
Revises: 
Create Date: 2024-01-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_style_config_column'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add style_config column
    op.add_column('presentations', sa.Column('style_config', sa.JSON(), nullable=True))


def downgrade():
    # Drop style_config column
    op.drop_column('presentations', 'style_config') 