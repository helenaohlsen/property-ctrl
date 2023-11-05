"""Create apartments table

Revision ID: cc02354d72d6
Revises: 7c3ae7e5afd1
Create Date: 2023-10-25 14:45:33.440236

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc02354d72d6'
down_revision: Union[str, None] = '7c3ae7e5afd1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'apartments',
        sa.Column('apartment_id', sa.Integer, primary_key=True),
        sa.Column('address', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime, default=datetime.datetime.utcnow),
        sa.Column('updated_at', sa.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow),
    )
    pass


def downgrade() -> None:
    pass
