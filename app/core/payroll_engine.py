"""
Payroll engine: orchestrates the calculation of gross pay, taxes,
deductions, and garnishments using strategy and service layers.
"""
from decimal import Decimal, ROUND_HALF_UP

from app.strategies.federal_tax import FederalTaxStrategy

from .models import PayInput, PayResult
from .validators import validate_pay_input
from ..strategies.factory import get_tax_strategy
from ..services.deduction_service import calculate_deductions
from ..services.garnishment_service import calculate_garnishments


def run_payroll(data: PayInput) -> PayResult:
    """
    Main entry point for payroll calculation.

    Steps:
    1. Validate input
    2. Compute gross pay
    3. Apply federal + state tax strategies
    4. Apply deductions
    5. Apply garnishments
    6. Return final PayResult
    """

    # 1. Validate input (raises ValueError if invalid)
    validate_pay_input(data)

    # 2. Gross pay gross_pay = data.hours_worked * data.pay_rate
    gross_pay = (Decimal(data.hours_worked) * Decimal(data.pay_rate)).quantize(
    Decimal("0.01"), rounding=ROUND_HALF_UP
    )

    # 3. Taxes (strategy pattern)
    tax_strategy = get_tax_strategy(data.work_state, data.home_state)
    state_taxes = tax_strategy.calculate(gross_pay, data)
    federal_taxes = FederalTaxStrategy().calculate(gross_pay, data)
    taxes = state_taxes + federal_taxes

    # 4. Deductions (service layer)
    deductions = calculate_deductions(data, gross_pay)

    # 5. Garnishments (service layer)
    garnishments = calculate_garnishments(data, gross_pay)

    # 6. Net pay
    net_pay = gross_pay - taxes - deductions - garnishments

    return PayResult(
        gross_pay=gross_pay,
        net_pay=net_pay,
        taxes=taxes,
        deductions=deductions,
        garnishments=garnishments,
    )
