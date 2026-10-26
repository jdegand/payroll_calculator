"""
Validation utilities for the payroll engine.

These functions enforce business rules that go beyond basic
Pydantic type validation. They ensure that payroll inputs
are logically valid before calculations begin.
"""

from decimal import Decimal
from .models import PayInput


# -----------------------------
# Basic numeric validations
# -----------------------------

def validate_hours(hours: Decimal) -> None:
    if hours < Decimal("0"):
        raise ValueError("Hours worked cannot be negative.")
    if hours > Decimal("168"):
        raise ValueError("Hours worked exceeds maximum allowed for a week.")


def validate_pay_rate(rate: Decimal) -> None:
    if rate < Decimal("0"):
        raise ValueError("Pay rate cannot be negative.")
    if rate > Decimal("1000"):
        raise ValueError("Pay rate is unreasonably high.")


# -----------------------------
# State validation
# -----------------------------

def validate_state(state: str) -> None:
    if len(state) != 2:
        raise ValueError("State must be a 2-letter code (e.g., 'CA', 'NY').")
    if not state.isalpha():
        raise ValueError("State code must contain only letters.")


# -----------------------------
# Federal tax realism validations
# -----------------------------

def validate_filing_status(status: str) -> None:
    if status not in {"single", "married"}:
        raise ValueError("Filing status must be 'single' or 'married'.")


def validate_pay_frequency(freq: str) -> None:
    valid = {"weekly", "biweekly", "semimonthly", "monthly"}
    if freq not in valid:
        raise ValueError(f"Pay frequency must be one of: {', '.join(valid)}")


def validate_dependents(dep: int) -> None:
    if dep < 0:
        raise ValueError("Dependents cannot be negative.")
    if dep > 20:
        raise ValueError("Dependents value is unrealistically high.")


def validate_additional_withholding(amount: Decimal) -> None:
    if amount < Decimal("0"):
        raise ValueError("Additional withholding cannot be negative.")
    if amount > Decimal("5000"):
        raise ValueError("Additional withholding is unreasonably high.")


# -----------------------------
# Pre-tax deduction validations
# -----------------------------

def validate_pretax_401k(rate: Decimal | None) -> None:
    if rate is None:
        return
    if rate < Decimal("0") or rate > Decimal("1"):
        raise ValueError("401k rate must be between 0.0 and 1.0 (e.g., 0.05 for 5%).")


def validate_fixed_amount(name: str, amount: Decimal | None) -> None:
    if amount is None:
        return
    if amount < Decimal("0"):
        raise ValueError(f"{name} cannot be negative.")
    if amount > Decimal("5000"):
        raise ValueError(f"{name} amount is unreasonably high.")


# -----------------------------
# Year-to-date income
# -----------------------------

def validate_ytd_income(ytd: Decimal) -> None:
    if ytd < Decimal("0"):
        raise ValueError("Year-to-date income cannot be negative.")
    if ytd > Decimal("1000000"):
        raise ValueError("Year-to-date income is unreasonably high.")


# -----------------------------
# Garnishment validations
# -----------------------------

def validate_garnishment_rate(rate: Decimal | None) -> None:
    if rate is None:
        return
    if rate < Decimal("0") or rate > Decimal("1"):
        raise ValueError("Garnishment rate must be between 0.0 and 1.0.")


# -----------------------------
# Main validation entry point
# -----------------------------

def validate_pay_input(data: PayInput) -> None:
    """
    Run all validation checks on the PayInput model.
    This is called by the payroll engine before processing.
    """

    # Basic pay validations
    validate_hours(data.hours_worked)
    validate_pay_rate(data.pay_rate)

    # State validations
    validate_state(data.work_state)
    validate_state(data.home_state)

    # Federal tax realism
    validate_filing_status(data.filing_status)
    validate_pay_frequency(data.pay_frequency)
    validate_dependents(data.dependents)
    validate_additional_withholding(data.additional_withholding)

    # Pre-tax deductions
    validate_pretax_401k(data.pretax_401k_rate)
    validate_fixed_amount("HSA amount", data.hsa_amount)
    validate_fixed_amount("FSA amount", data.fsa_amount)

    # YTD income
    validate_ytd_income(data.ytd_income)

    # Post-tax deductions
    validate_fixed_amount("Union dues", data.union_dues)
    if data.voluntary_deductions:
        for d in data.voluntary_deductions:
            validate_fixed_amount("Voluntary deduction", d)

    # Garnishments
    validate_fixed_amount("Child support amount", data.child_support_amount)
    validate_garnishment_rate(data.child_support_rate)
    validate_fixed_amount("Tax levy amount", data.tax_levy_amount)
    validate_garnishment_rate(data.creditor_garnishment_rate)
