"""Add content column to post table

Revision ID: b6f01335ad6f
Revises: 2a5bba6c45ce
Create Date: 2023-11-19 20:54:54.132853

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6f01335ad6f'
down_revision: Union[str, None] = '2a5bba6c45ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
