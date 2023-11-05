"""Create renters table

Revision ID: 7340ec0c2830
Revises: cc02354d72d6
Create Date: 2023-10-25 15:05:19.385180

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7340ec0c2830'
down_revision: Union[str, None] = 'cc02354d72d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'renters',
        sa.Column('renter_id', sa.Integer, primary_key=True),
        sa.Column('renter_firstname', sa.String(50)),
        sa.Column('renter_lastname', sa.String(100)),
        sa.Column('created_at', sa.DateTime, default=datetime.datetime.utcnow),
        sa.Column('updated_at', sa.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow),
    )
    pass


def downgrade() -> None:
    pass
