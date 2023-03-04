"""add phone number to the post table

Revision ID: e68830f796b0
Revises: cbce4e072baa
Create Date: 2023-03-03 20:50:00.082836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e68830f796b0'
down_revision = 'cbce4e072baa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('contact_number', sa.String(),nullable= True))
    pass


def downgrade() -> None:
    op.drop_column('posts','contact_number')
    pass
