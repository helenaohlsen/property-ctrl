"""Create leases table

Revision ID: f11c90d308b2
Revises: 7340ec0c2830
Create Date: 2023-10-25 15:09:05.186323

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f11c90d308b2'
down_revision: Union[str, None] = '7340ec0c2830'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'leases',
        sa.Column('lease_id', sa.Integer, primary_key=True),
        sa.Column('apartment_id', sa.Integer, sa.ForeignKey('apartments.apartment_id')),
        sa.Column('renter_id', sa.Integer, sa.ForeignKey('renters.renter_id')),
        sa.Column('start_date', sa.Date),
        sa.Column('end_date', sa.Date),
        sa.Column('price', sa.Numeric(precision=6, scale=2)),
        sa.Column('created_at', sa.DateTime, default=datetime.datetime.utcnow),
        sa.Column('updated_at', sa.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow),
    )
    pass


def downgrade() -> None:
    pass
