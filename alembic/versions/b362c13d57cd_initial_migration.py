"""Initial migration

Revision ID: b362c13d57cd
Revises: 
Create Date: 2025-04-19 09:07:15.547009

"""
from typing import Sequence, Union
from pydantic import EmailStr

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b362c13d57cd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('published', sa.Boolean(), nullable=False, server_default=sa.text('true')),
                    sa.Column('rating', sa.Float(), nullable=True),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), onupdate=sa.text('CURRENT_TIMESTAMP'), nullable=True),
                    schema='public'
                    )

def downgrade() -> None:
    """Downgrade schema."""
    pass
