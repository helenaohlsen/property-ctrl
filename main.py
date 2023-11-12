from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder

from app.deps import get_db
from app.db.db import (
    db_create_obj,
    db_find_by_id,
    db_get_apartments,
    db_query,
    db_update_obj,
)
from app.db.session import SessionLocal
from app.models import Apartments as ModelApartments
from app.models import Leases as ModelLeases
from app.models import Renters as ModelRenters
from app.schemas import (
    Apartment,
    ApartmentCreate,
    ApartmentPagination,
    Lease,
    LeaseCreate,
    LeasePagination,
    LeaseUpdate,
    Renter,
    RenterCreate,
    RenterPagination,
)

app = FastAPI()


@app.get("/apartments", response_model=ApartmentPagination)
def get_apartments(
    *,
    page: int = 1,
    items_per_page: int = 10,
    vacant: bool = False,
    db: SessionLocal = Depends(get_db),
):
    return db_get_apartments(
        page=page, items_per_page=items_per_page, vacant=vacant, db=db
    )


@app.post("/apartments", response_model=Apartment)
def create_apartment(
    *, db: SessionLocal = Depends(get_db), apartment_in: ApartmentCreate
) -> Any:
    """
    Create new apartment.
    """
    obj_in_data = jsonable_encoder(apartment_in)
    return db_create_obj(obj_in_data, ModelApartments, db=db)


@app.get("/renters", response_model=RenterPagination)
def get_renters(
    *, page: int = 1, items_per_page: int = 10, db: SessionLocal = Depends(get_db)
):
    query = db.query(ModelRenters)

    return db_query(query, page, items_per_page, db=db)


@app.post("/renters", response_model=Renter)
def create_renter(
    *, db: SessionLocal = Depends(get_db), renter_in: RenterCreate
) -> Any:
    """
    Create new renter.
    """
    obj_in_data = jsonable_encoder(renter_in)
    return db_create_obj(obj_in_data, ModelRenters, db=db)


@app.get("/leases", response_model=LeasePagination)
def get_leases(
    *, page: int = 1, items_per_page: int = 10, db: SessionLocal = Depends(get_db)
):
    query = db.query(ModelLeases)
    return db_query(query, page, items_per_page, db=db)


@app.post("/leases", response_model=Lease)
def create_lease(*, db: SessionLocal = Depends(get_db), lease_in: LeaseCreate) -> Any:
    """
    Create new lease.
    """
    obj_in_data = jsonable_encoder(lease_in)
    db_obj = ModelLeases(**obj_in_data)

    renter_id, apartment_id = db_obj.renter_id, db_obj.apartment_id

    renter = db_find_by_id(ModelRenters, renter_id, db=db)
    if not renter:
        raise HTTPException(
            status_code=404, detail=f"Renter with id {renter_id} not found"
        )

    apartment = db_find_by_id(ModelApartments, apartment_id, db=db)
    if not apartment:
        raise HTTPException(
            status_code=404, detail=f"Apartment with id {apartment_id} not found"
        )
    return db_create_obj(obj_in_data, ModelLeases, db=db)


@app.put("/leases/{lease_id}", response_model=Lease)
def update_lease(
    *, db: SessionLocal = Depends(get_db), lease_id: int, lease_in: LeaseUpdate
) -> Any:
    """
    Update a lease.
    """
    obj_data = jsonable_encoder(lease_in)
    lease = db_find_by_id(ModelLeases, lease_id, db=db)

    if not lease:
        raise HTTPException(status_code=404, detail=f"Lease {lease_id} not found")

    if isinstance(lease_in, dict):
        update_data = lease_in
    else:
        update_data = lease_in.model_dump(exclude_unset=True)

    return db_update_obj(obj_data, update_data, lease, db=db)
