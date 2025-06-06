"""auto-create votes table

Revision ID: de3b044a5dc7
Revises: c44c38d35ee6
Create Date: 2025-04-20 11:48:59.503986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'de3b044a5dc7'
down_revision: Union[str, None] = 'c44c38d35ee6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['public.posts.id'], name='fk_votes_posts_id', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['public.users.id'], name='fk_votes_users_id', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('post_id', 'user_id'),
    schema='public'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('votes', schema='public')
    # ### end Alembic commands ###
