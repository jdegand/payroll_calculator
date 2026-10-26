"""
Deduction service.

Handles:
- Pre-tax deductions (e.g., 401k, HSA, FSA)
- Post-tax deductions (e.g., union dues, voluntary deductions)
"""

from decimal import Decimal, ROUND_HALF_UP
from ..core.models import PayInput


def calculate_pre_tax_deductions(data: PayInput, gross_pay: Decimal) -> Decimal:
    """
    Calculate pre-tax deductions using Decimal.
    - 401k: percentage of gross pay
    - HSA: fixed amount
    - FSA: fixed amount
    """

    deductions = Decimal("0.00")

    # 401k percentage
    if data.pretax_401k_rate:
        deductions += gross_pay * data.pretax_401k_rate

    # HSA fixed amount
    if data.hsa_amount:
        deductions += data.hsa_amount

    # FSA fixed amount
    if data.fsa_amount:
        deductions += data.fsa_amount

    return deductions.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_post_tax_deductions(data: PayInput) -> Decimal:
    """
    Calculate post-tax deductions using Decimal.
    - Union dues
    - Misc voluntary deductions
    """

    deductions = Decimal("0.00")

    # Union dues
    if data.union_dues:
        deductions += data.union_dues

    # Voluntary deductions list
    if data.voluntary_deductions:
        for d in data.voluntary_deductions:
            deductions += d

    return deductions.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_deductions(data: PayInput, gross_pay: Decimal) -> Decimal:
    """
    Total deductions = pre-tax + post-tax.
    """

    pre_tax = calculate_pre_tax_deductions(data, gross_pay)
    post_tax = calculate_post_tax_deductions(data)

    total = pre_tax + post_tax

    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
