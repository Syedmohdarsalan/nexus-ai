"""Create and read invoices; no payment execution is available."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .database import get_db
from .models import Invoice
from .schemas import InvoiceCreate, InvoiceRead

router = APIRouter(prefix="/api/v1/invoices", tags=["Invoices"])

@router.post("", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
def create_invoice(payload: InvoiceCreate, db: Session = Depends(get_db)):
    invoice = Invoice(**payload.model_dump())
    db.add(invoice)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        duplicate = db.scalar(select(Invoice.id).where(
            Invoice.vendor_name == payload.vendor_name,
            Invoice.invoice_number == payload.invoice_number,
        ))
        if duplicate is not None:
            raise HTTPException(status_code=409, detail="Invoice number already exists for this vendor.") from None
        raise
    db.refresh(invoice)
    return invoice

@router.get("", response_model=list[InvoiceRead])
def list_invoices(
    limit: int = Query(100, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return db.scalars(select(Invoice).order_by(Invoice.id).offset(offset).limit(limit)).all()

@router.get("/{invoice_id}", response_model=InvoiceRead)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.get(Invoice, invoice_id)
    if invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found.")
    return invoice
