from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.db.config import (
    MAX_APARTMENT_ADDRESS_LEN,
    MAX_RENTER_FIRSTNAME_LEN,
    MAX_RENTER_LASTNAME_LEN,
)


class Apartments(Base):
    apartment_id = Column(Integer, primary_key=True)
    address = Column(String(MAX_APARTMENT_ADDRESS_LEN))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    leases = relationship("Leases", back_populates="apartment")


class Renters(Base):
    renter_id = Column(Integer, primary_key=True)
    renter_firstname = Column(String(MAX_RENTER_FIRSTNAME_LEN))
    renter_lastname = Column(String(MAX_RENTER_LASTNAME_LEN))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    leases = relationship("Leases", back_populates="renter")


class Leases(Base):
    lease_id = Column(Integer, primary_key=True)
    apartment_id = Column(
        Integer, ForeignKey("apartments.apartment_id"), nullable=False
    )
    renter_id = Column(Integer, ForeignKey("renters.renter_id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    price = Column(Numeric(precision=5, scale=2))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    apartment = relationship("Apartments", back_populates="leases")
    renter = relationship("Renters", back_populates="leases")
