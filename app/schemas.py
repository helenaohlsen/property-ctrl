from datetime import date, datetime
from typing import List
from pydantic import BaseModel, Field
from decimal import Decimal

from app.db.config import (
    MAX_APARTMENT_ADDRESS_LEN,
    MAX_RENTER_FIRSTNAME_LEN,
    MAX_RENTER_LASTNAME_LEN,
)


class Pagination(BaseModel):
    itemsPerPage: int
    page: int
    total: int


class ApartmentCreate(BaseModel):
    address: str = Field(max_length=MAX_APARTMENT_ADDRESS_LEN)


class Apartment(ApartmentCreate):
    apartment_id: int
    created_at: datetime
    updated_at: datetime


class ApartmentPagination(Pagination):
    items: List[Apartment]


class RenterCreate(BaseModel):
    renter_firstname: str = Field(max_length=MAX_RENTER_FIRSTNAME_LEN)
    renter_lastname: str = Field(max_length=MAX_RENTER_LASTNAME_LEN)


class Renter(RenterCreate):
    renter_id: int
    created_at: datetime
    updated_at: datetime


class RenterPagination(Pagination):
    items: List[Renter]


class LeaseCreate(BaseModel):
    renter_id: int
    apartment_id: int
    start_date: date
    end_date: date
    price: Decimal = Field(ge=0.01, decimal_places=2)


class Lease(LeaseCreate):
    lease_id: int
    created_at: datetime
    updated_at: datetime


class LeasePagination(Pagination):
    items: List[Lease]


class LeaseUpdate(BaseModel):
    end_date: date
    price: Decimal = Field(ge=0.01, decimal_places=2)
