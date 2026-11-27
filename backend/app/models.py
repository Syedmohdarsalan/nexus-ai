"""Persistent invoice model. Money is stored in integer minor units (paise/cents)."""
from datetime import date
from sqlalchemy import BigInteger, CheckConstraint, Date, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Invoice(Base):
    __tablename__ = "invoices"
    __table_args__ = (
        UniqueConstraint("vendor_name", "invoice_number", name="uq_vendor_invoice"),
        CheckConstraint("amount_minor > 0", name="ck_positive_amount"),
        CheckConstraint("currency IN ('INR','USD','EUR')", name="ck_currency"),
        CheckConstraint("status = 'pending_review'", name="ck_initial_status"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_number: Mapped[str] = mapped_column(String(80))
    vendor_name: Mapped[str] = mapped_column(String(120))
    amount_minor: Mapped[int] = mapped_column(BigInteger)
    currency: Mapped[str] = mapped_column(String(3))
    due_date: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(30), default="pending_review")
