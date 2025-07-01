"""delete dir from votes table

Revision ID: cbccab4c3576
Revises: 13447d78e17e
Create Date: 2025-07-01 11:32:54.903173

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cbccab4c3576'
down_revision: Union[str, Sequence[str], None] = '13447d78e17e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('votes',
                   'dir')
    pass


def downgrade() -> None:
    op.add_column('votes',sa.Column('dir',sa.Integer))
    pass
