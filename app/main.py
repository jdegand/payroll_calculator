"""
Simple CLI entry point for testing the payroll engine.
"""

from decimal import Decimal
from app.core.models import PayInput
from app.core.payroll_engine import run_payroll


def main():
    data = PayInput(
        employee_id="123",
        hours_worked=Decimal("40"),
        pay_rate=Decimal("25.00"),

        # Jurisdiction
        work_state="NJ",
        home_state="PA",

        # Federal tax realism
        filing_status="single",
        pay_frequency="weekly",
        dependents=1,
        additional_withholding=Decimal("10.00"),

        # Pre‑tax deductions
        pretax_401k_rate=Decimal("0.05"),
        hsa_amount=Decimal("20.00"),
        fsa_amount=Decimal("0.00"),

        # Year‑to‑date income
        ytd_income=Decimal("15000.00"),

        # Optional post‑tax deductions
        union_dues=Decimal("0.00"),
        voluntary_deductions=[Decimal("5.00")],

        # Optional garnishments
        child_support_amount=Decimal("0.00"),
        tax_levy_amount=Decimal("0.00"),
    )

    result = run_payroll(data)
    print(result.model_dump())


if __name__ == "__main__":
    main()
