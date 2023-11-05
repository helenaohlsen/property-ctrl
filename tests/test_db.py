from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.db import db_create_obj, db_get_apartments
from app.models import Apartments as ModelApartments
from app.models import Base
from app.models import Leases as ModelLeases
from app.models import Renters as ModelRenters
from main import app

client = TestClient(app)


# Unittests exclusively for the db operations
# tests for the routes come later in a separate file


@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///:memory:", echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    # When a fixture includes a yield statement, Pytest treats the code before the yield
    # as setup logic and the code after the yield as teardown logic
    yield SessionLocal
    Base.metadata.drop_all(bind=engine)


test_cases = [
    {
        "apartments": [],
        "vacant_filter": False,
        "expected_len": 0,
        "expected_addresses": [],
    },
    {
        "apartments": [{"address": "example1", "vacant": True}],
        "vacant_filter": False,
        "expected_len": 1,
        "expected_addresses": ["example1"],
    },
    {
        "apartments": [{"address": "example2", "vacant": True}],
        "vacant_filter": True,
        "expected_len": 1,
        "expected_addresses": ["example2"],
    },
    {
        "apartments": [{"address": "example3", "vacant": False}],
        "vacant_filter": False,
        "expected_len": 1,
        "expected_addresses": ["example3"],
    },
    {
        "apartments": [{"address": "example4", "vacant": False}],
        "vacant_filter": True,
        "expected_len": 0,
        "expected_addresses": [],
    },
    {
        "apartments": [
            {"address": "example5_1", "vacant": True},
            {"address": "example5_2", "vacant": True},
        ],
        "vacant_filter": False,
        "expected_len": 2,
        "expected_addresses": ["example5_1", "example5_2"],
    },
    {
        "apartments": [
            {"address": "example6_1", "vacant": True},
            {"address": "example6_2", "vacant": True},
        ],
        "vacant_filter": True,
        "expected_len": 2,
        "expected_addresses": ["example6_1", "example6_2"],
    },
    {
        "apartments": [
            {"address": "example7_1", "vacant": True},
            {"address": "example7_2", "vacant": False},
        ],
        "vacant_filter": False,
        "expected_len": 2,
        "expected_addresses": ["example7_1", "example7_2"],
    },
    {
        "apartments": [
            {"address": "example8_1", "vacant": True},
            {"address": "example8_2", "vacant": False},
        ],
        "vacant_filter": True,
        "expected_len": 1,
        "expected_addresses": ["example8_1"],
    },
    {
        "apartments": [
            {"address": "example9_1", "vacant": False},
            {"address": "example9_2", "vacant": False},
        ],
        "vacant_filter": False,
        "expected_len": 2,
        "expected_addresses": ["example9_1", "example9_2"],
    },
    {
        "apartments": [
            {"address": "example10_2", "vacant": False},
            {"address": "example10_2", "vacant": False},
        ],
        "vacant_filter": True,
        "expected_len": 0,
        "expected_addresses": [],
    },
]


@pytest.mark.parametrize("test_case", test_cases)
def test_db_get_apartments(test_case, test_db):
    session = test_db()
    for apartment in test_case["apartments"]:
        db_apartment = db_create_obj(
            {"address": apartment["address"]}, ModelApartments, session
        )
        if not apartment["vacant"]:
            renter_db = db_create_obj(
                {"renter_firstname": "first", "renter_lastname": "last"},
                ModelRenters,
                session,
            )
            lease_in = {
                "apartment_id": db_apartment.apartment_id,
                "renter_id": renter_db.renter_id,
                "start_date": datetime(2023, 10, 1),
                "end_date": datetime(2024, 12, 1),
                "price": 200.99,
            }
            db_create_obj(lease_in, ModelLeases, session)

    result = db_get_apartments(
        page=1, items_per_page=10, vacant=test_case["vacant_filter"], db=session
    )
    items = result.get("items")
    assert len(items) == test_case["expected_len"]
    addresses = [item.address for item in items]
    assert addresses == test_case["expected_addresses"]
