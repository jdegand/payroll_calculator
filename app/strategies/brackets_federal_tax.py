from .base_tax_strategy import BaseTaxStrategy
from ..core.models import PayInput

# Simplified IRS marginal brackets (single filer)
FEDERAL_BRACKETS = [
    (0,       0.10),
    (11000,   0.12),
    (44725,   0.22),
    (95375,   0.24),
    (182100,  0.32),
    (231250,  0.35),
    (578125,  0.37),
]


class FederalTaxStrategy(BaseTaxStrategy):

    def calculate(self, gross_pay: float, data: PayInput) -> float:
        """
        Realistic federal withholding:
        1. Annualize pay
        2. Apply marginal tax brackets
        3. Convert back to per-paycheck withholding
        """

        # Assume weekly pay for now (you can make this configurable)
        annualized_income = gross_pay * 52

        annual_tax = self._apply_brackets(annualized_income)

        # Convert back to weekly withholding
        return annual_tax / 52

    def _apply_brackets(self, income: float) -> float:
        tax = 0.0

        for i in range(len(FEDERAL_BRACKETS)):
            threshold, rate = FEDERAL_BRACKETS[i]

            # Last bracket
            if i == len(FEDERAL_BRACKETS) - 1:
                tax += (income - threshold) * rate
                break

            next_threshold = FEDERAL_BRACKETS[i + 1][0]

            if income > threshold:
                taxable_amount = min(income, next_threshold) - threshold
                tax += taxable_amount * rate

        return max(tax, 0.0)
