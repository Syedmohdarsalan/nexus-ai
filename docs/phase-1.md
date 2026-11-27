# Phase 1.1 — Foundation

Implemented: local API, invoice schema, SQLite migration, create/list/retrieve endpoints, validation, exact duplicate constraint, tests.

Next: CSV ingestion, row-level error reports, vendor normalization and explainable fraud rules. Exact duplicate prevention is not a fraud model. An invoice is always pending review in this release. All data is synthetic. No authentication, production deployment, payment provider, LLM, frontend or real payment execution is implemented. Do not expose this local API publicly.

The amount_minor column stores integer paise/cents. INR, USD and EUR are the only supported currencies initially. ₹25,000 = 2500000 paise. Exact vendor name + invoice number is the duplicate key; case variants and lookalikes are not yet detected.
