"""create users table

Revision ID: c44c38d35ee6
Revises: b362c13d57cd
Create Date: 2025-04-20 08:14:07.627378

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c44c38d35ee6'
down_revision: Union[str, None] = 'b362c13d57cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
                sa.Column('id',sa.Integer(), primary_key=True, nullable=False),
                sa.Column('email', sa.String(), unique=True, nullable=False),
                sa.Column('password', sa.String(), nullable=False),
                sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=True)
                # sa.Column('userrole_id', sa.Integer(), sa.ForeignKey('parametrics.userrole.id', ondelete='SET DEFAULT'), nullable=True),
                # schema='public'
                )
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=True), schema='public')
    op.create_foreign_key('fk_posts_user_id',
                    'posts',
                    'users',
                    ['user_id'],
                    ['id'],
                    ondelete='SET NULL'
                )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users', schema='public')
    op.drop_constraint('fk_posts_user_id', 'posts', type_='foreignkey', schema='public')
    op.drop_column('posts', 'user_id', schema='public')