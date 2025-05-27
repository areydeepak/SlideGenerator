"""add content and slides_data fields

Revision ID: add_content_and_slides_data
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_content_and_slides_data'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add content column
    op.add_column('presentations', sa.Column('content', sa.Text(), nullable=True))
    
    # Add slides_data column
    op.add_column('presentations', sa.Column('slides_data', sa.JSON(), nullable=True))
    
    # Drop config column if it exists
    op.drop_column('presentations', 'config')
    
    # Make content non-nullable after populating existing rows
    op.execute("UPDATE presentations SET content = topic WHERE content IS NULL")
    op.alter_column('presentations', 'content', nullable=False)


def downgrade():
    # Add back config column
    op.add_column('presentations', sa.Column('config', sa.JSON(), nullable=True))
    
    # Drop slides_data column
    op.drop_column('presentations', 'slides_data')
    
    # Drop content column
    op.drop_column('presentations', 'content') 