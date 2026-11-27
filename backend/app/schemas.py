"""Pydantic validates JSON before it reaches the database."""
from datetime import date
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator

class InvoiceCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    invoice_number: str = Field(min_length=1, max_length=80)
    vendor_name: str = Field(min_length=1, max_length=120)
    amount_minor: int = Field(gt=0, le=10**12, strict=True)
    currency: Literal["INR", "USD", "EUR"]
    due_date: date

    @field_validator("currency", mode="before")
    @classmethod
    def normalize_currency(cls, value):
        return value.strip().upper() if isinstance(value, str) else value

class InvoiceRead(InvoiceCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: Literal["pending_review"]
