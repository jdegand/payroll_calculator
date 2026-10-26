"""
New Jersey state income tax strategy.

NJ has progressive brackets.
"""

from decimal import Decimal, ROUND_HALF_UP
from ..base_tax_strategy import BaseTaxStrategy
from ...core.models import PayInput


# New Jersey graduated income tax brackets (single filer)
# All values are Decimal for payroll‑safe precision
NJ_BRACKETS = [
    (Decimal("0"),        Decimal("0.0140")),   # 1.4% on $0 – $20,000
    (Decimal("20000"),    Decimal("0.0175")),   # 1.75% on $20,001 – $35,000
    (Decimal("35000"),    Decimal("0.0350")),   # 3.5% on $35,001 – $40,000
    (Decimal("40000"),    Decimal("0.05525")),  # 5.525% on $40,001 – $75,000
    (Decimal("75000"),    Decimal("0.0637")),   # 6.37% on $75,001 – $500,000
    (Decimal("500000"),   Decimal("0.0897")),   # 8.97% on $500,001 – $1,000,000
    (Decimal("1000000"),  Decimal("0.1075")),   # 10.75% on $1,000,001+
]


class NewJerseyTaxStrategy(BaseTaxStrategy):

    def calculate(self, gross_pay: Decimal, data: PayInput) -> Decimal:
        """
        Realistic NJ state withholding:
        1. Annualize taxable wages
        2. Apply NJ graduated brackets
        3. De-annualize back to per-paycheck withholding
        """

        # Annualize based on pay frequency
        multiplier = {
            "weekly": 52,
            "biweekly": 26,
            "semimonthly": 24,
            "monthly": 12,
        }.get(data.pay_frequency, 52)

        annualized_income = gross_pay * Decimal(multiplier)

        annual_tax = self._apply_brackets(annualized_income)

        per_period_tax = annual_tax / Decimal(multiplier)

        return per_period_tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def _apply_brackets(self, income: Decimal) -> Decimal:
        tax = Decimal("0.00")

        for i in range(len(NJ_BRACKETS)):
            threshold, rate = NJ_BRACKETS[i]

            # Last bracket
            if i == len(NJ_BRACKETS) - 1:
                tax += (income - threshold) * rate
                break

            next_threshold = NJ_BRACKETS[i + 1][0]

            if income > threshold:
                taxable_amount = min(income, next_threshold) - threshold
                tax += taxable_amount * rate

        return tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
