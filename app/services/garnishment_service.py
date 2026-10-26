"""
Garnishment service.

Handles:
- Child support
- Tax levies
- Creditor garnishments
"""

from decimal import Decimal, ROUND_HALF_UP
from ..core.models import PayInput


def calculate_child_support(data: PayInput, gross_pay: Decimal) -> Decimal:
    """
    Child support can be:
    - A fixed amount
    - A percentage of gross pay
    """

    # Fixed amount takes priority
    if data.child_support_amount:
        return data.child_support_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # Percentage of gross pay
    if data.child_support_rate:
        amount = gross_pay * data.child_support_rate
        return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return Decimal("0.00")


def calculate_tax_levy(data: PayInput, gross_pay: Decimal) -> Decimal:
    """
    Tax levy is usually a fixed amount.
    """

    if data.tax_levy_amount:
        return data.tax_levy_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return Decimal("0.00")


def calculate_creditor_garnishment(data: PayInput, gross_pay: Decimal) -> Decimal:
    """
    Creditor garnishment is typically a percentage of disposable income.
    """

    if data.creditor_garnishment_rate:
        amount = gross_pay * data.creditor_garnishment_rate
        return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return Decimal("0.00")


def calculate_garnishments(data: PayInput, gross_pay: Decimal) -> Decimal:
    """
    Total garnishments = child support + tax levy + creditor garnishment.
    """

    child_support = calculate_child_support(data, gross_pay)
    tax_levy = calculate_tax_levy(data, gross_pay)
    creditor = calculate_creditor_garnishment(data, gross_pay)

    total = child_support + tax_levy + creditor

    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
