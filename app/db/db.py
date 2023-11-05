from datetime import datetime

from fastapi import Depends
from sqlalchemy import inspect, not_
from sqlalchemy_filters import apply_pagination

from app.deps import get_db
from app.db.session import SessionLocal
from app.models import Apartments as ModelApartments
from app.models import Leases as ModelLeases


def db_create_obj(obj_in_data, db_model, db: SessionLocal = Depends(get_db)):
    db_obj = db_model(**obj_in_data)
    now = datetime.utcnow()
    db_obj.created_at, db_obj.updated_at = now, now
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def db_query(db_query, page, items_per_page, db: SessionLocal = Depends(get_db)):
    query, pagination = apply_pagination(
        db_query, page_number=page, page_size=items_per_page
    )
    return {
        "items": query.all(),
        "itemsPerPage": pagination.page_size,
        "page": pagination.page_number,
        "total": pagination.total_results,
    }


def db_get_apartments(
    page: int,
    items_per_page: int,
    vacant: bool,
    db: SessionLocal = Depends(get_db),
):
    if vacant:
        query = (
            db.query(ModelApartments)
            .outerjoin(ModelLeases)
            .filter(not_(ModelLeases.apartment_id.isnot(None)))
        )
    else:
        query = db.query(ModelApartments)

    return db_query(query, page, items_per_page, db=db)


def db_find_by_id(db_model, id, db: SessionLocal = Depends(get_db)):
    db_model_field = getattr(db_model, get_id_column_name(db_model))
    return db.query(db_model).filter(db_model_field == id).first()


def db_update_obj(obj_data, update_data, db_obj, db: SessionLocal = Depends(get_db)):
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db_obj.updated_at = datetime.utcnow()

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_id_column_name(model):
    inspector = inspect(model)
    for col in inspector.c:
        if col.name.endswith("_id"):
            return col.name
