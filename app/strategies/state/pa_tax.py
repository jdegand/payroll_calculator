"""
Pennsylvania state income tax strategy.
"""

from decimal import Decimal, ROUND_HALF_UP
from ..base_tax_strategy import BaseTaxStrategy
from ...core.models import PayInput


class PennsylvaniaTaxStrategy(BaseTaxStrategy):
    PA_RATE = Decimal("0.0307")  # 3.07%

    def calculate(self, gross_pay: Decimal, data: PayInput) -> Decimal:
        """
        PA uses a flat 3.07% tax rate on taxable wages.
        """

        tax = gross_pay * self.PA_RATE

        # Payroll requires rounding to nearest cent using ROUND_HALF_UP
        return tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
