"""Create the initial invoice table."""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "invoices",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("invoice_number", sa.String(80), nullable=False),
        sa.Column("vendor_name", sa.String(120), nullable=False),
        sa.Column("amount_minor", sa.BigInteger(), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        sa.UniqueConstraint("vendor_name", "invoice_number", name="uq_vendor_invoice"),
        sa.CheckConstraint("amount_minor > 0", name="ck_positive_amount"),
        sa.CheckConstraint("currency IN ('INR','USD','EUR')", name="ck_currency"),
        sa.CheckConstraint("status = 'pending_review'", name="ck_initial_status"),
    )

def downgrade():
    op.drop_table("invoices")
