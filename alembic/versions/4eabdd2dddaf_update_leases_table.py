"""Update leases table

Revision ID: 4eabdd2dddaf
Revises: f11c90d308b2
Create Date: 2023-10-25 15:18:11.653553

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4eabdd2dddaf'
down_revision: Union[str, None] = 'f11c90d308b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('leases', 'apartment_id', existing_type=sa.Integer, nullable=False)
    op.alter_column('leases', 'renter_id', existing_type=sa.Integer, nullable=False)
    op.alter_column('leases', 'start_date', existing_type=sa.Date, nullable=False)
    op.alter_column('leases', 'price', existing_type=sa.Numeric(precision=6, scale=2), nullable=False)
    


def downgrade() -> None:
    op.alter_column('leases', 'apartment_id', existing_type=sa.Integer, nullable=True)
    op.alter_column('leases', 'renter_id', existing_type=sa.Integer, nullable=True)
    op.alter_column('leases', 'start_date', existing_type=sa.Date, nullable=True)
    op.alter_column('leases', 'price', existing_type=sa.Numeric(precision=6, scale=2), nullable=True)
    

