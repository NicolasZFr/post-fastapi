"""auto-add column phone_number

Revision ID: b92465c802ba
Revises: de3b044a5dc7
Create Date: 2025-04-20 12:06:15.692715

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'b92465c802ba'
down_revision: Union[str, None] = 'de3b044a5dc7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone_number', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###
