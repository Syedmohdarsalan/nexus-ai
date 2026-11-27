import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from app.database import Base, get_db
from app.main import app

PAYLOAD = {"invoice_number": "INV-001", "vendor_name": "Demo Cloud Services", "amount_minor": 2500000, "currency": "INR", "due_date": "2026-12-15"}

@pytest.fixture
def client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    def test_db():
        with Session(engine) as session:
            yield session
    app.dependency_overrides[get_db] = test_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        engine.dispose()

def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}

def test_create_and_retrieve_invoice(client):
    response = client.post("/api/v1/invoices", json=PAYLOAD)
    assert response.status_code == 201
    invoice = response.json()
    assert invoice["status"] == "pending_review"
    assert invoice["amount_minor"] == 2500000
    assert client.get(f"/api/v1/invoices/{invoice['id']}").json() == invoice
    assert client.get("/api/v1/invoices").json() == [invoice]

def test_duplicate_invoice(client):
    assert client.post("/api/v1/invoices", json=PAYLOAD).status_code == 201
    assert client.post("/api/v1/invoices", json=PAYLOAD).status_code == 409

def test_same_number_different_vendor(client):
    assert client.post("/api/v1/invoices", json=PAYLOAD).status_code == 201
    assert client.post("/api/v1/invoices", json={**PAYLOAD, "vendor_name": "Other Demo Vendor"}).status_code == 201

@pytest.mark.parametrize("patch", [{"amount_minor": 0}, {"amount_minor": -1}, {"amount_minor": 10.5}, {"currency": "XYZ"}, {"due_date": "invalid"}, {"status": "paid"}])
def test_invalid_invoice(client, patch):
    assert client.post("/api/v1/invoices", json={**PAYLOAD, **patch}).status_code == 422

def test_missing_invoice(client):
    assert client.get("/api/v1/invoices/999").status_code == 404

def test_empty_list(client):
    assert client.get("/api/v1/invoices").json() == []
