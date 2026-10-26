"""
Simple placeholder federal tax strategy.

This is intentionally minimal — real federal tax logic
will be more complex (brackets, FICA, Medicare, etc.).
"""

from .base_tax_strategy import BaseTaxStrategy
from ..core.models import PayInput


class FederalTaxStrategy(BaseTaxStrategy):
    FEDERAL_RATE = 0.10  # placeholder 10%

    def calculate(self, gross_pay: float, data: PayInput) -> float:
        return gross_pay * self.FEDERAL_RATE
