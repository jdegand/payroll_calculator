from decimal import Decimal, ROUND_HALF_UP
from .base_tax_strategy import BaseTaxStrategy
from ..core.models import PayInput


# IRS‑style marginal brackets (converted to Decimal)
FEDERAL_BRACKETS_SINGLE = [
    (Decimal("0"),        Decimal("0.10")),
    (Decimal("11000"),    Decimal("0.12")),
    (Decimal("44725"),    Decimal("0.22")),
    (Decimal("95375"),    Decimal("0.24")),
    (Decimal("182100"),   Decimal("0.32")),
    (Decimal("231250"),   Decimal("0.35")),
    (Decimal("578125"),   Decimal("0.37")),
]

FEDERAL_BRACKETS_MARRIED = [
    (Decimal("0"),        Decimal("0.10")),
    (Decimal("22000"),    Decimal("0.12")),
    (Decimal("89450"),    Decimal("0.22")),
    (Decimal("190750"),   Decimal("0.24")),
    (Decimal("364200"),   Decimal("0.32")),
    (Decimal("462500"),   Decimal("0.35")),
    (Decimal("693750"),   Decimal("0.37")),
]

# Standard deduction (2024)
STANDARD_DEDUCTION = {
    "single": Decimal("14600"),
    "married": Decimal("29200"),
}

# Pay frequency multipliers
PAY_FREQUENCY_MULTIPLIER = {
    "weekly": 52,
    "biweekly": 26,
    "semimonthly": 24,
    "monthly": 12,
}


class FederalTaxStrategy(BaseTaxStrategy):

    def calculate(self, gross_pay: Decimal, data: PayInput) -> Decimal:
        """
        Realistic federal withholding using Decimal:
        1. Apply pre-tax deductions
        2. Annualize wages
        3. Subtract standard deduction
        4. Apply marginal tax brackets
        5. De-annualize
        6. Apply dependent credits
        7. Add additional withholding
        """

        # -----------------------------
        # 1. Pre‑tax adjustments
        # -----------------------------
        taxable_wages = gross_pay

        if data.pretax_401k_rate:
            taxable_wages -= gross_pay * data.pretax_401k_rate

        if data.hsa_amount:
            taxable_wages -= data.hsa_amount

        if data.fsa_amount:
            taxable_wages -= data.fsa_amount

        taxable_wages = max(taxable_wages, Decimal("0.00"))

        # -----------------------------
        # 2. Annualize
        # -----------------------------
        multiplier = PAY_FREQUENCY_MULTIPLIER.get(data.pay_frequency, 52)
        multiplier_dec = Decimal(multiplier)

        annualized_income = taxable_wages * multiplier_dec

        # -----------------------------
        # 3. Subtract standard deduction
        # -----------------------------
        annualized_income -= STANDARD_DEDUCTION[data.filing_status]
        annualized_income = max(annualized_income, Decimal("0.00"))

        # -----------------------------
        # 4. Apply marginal brackets
        # -----------------------------
        brackets = (
            FEDERAL_BRACKETS_SINGLE
            if data.filing_status == "single"
            else FEDERAL_BRACKETS_MARRIED
        )

        annual_tax = self._apply_brackets(annualized_income, brackets)

        # -----------------------------
        # 5. De‑annualize
        # -----------------------------
        per_period_tax = annual_tax / multiplier_dec

        # -----------------------------
        # 6. Dependent credit (W‑4 Step 3)
        # -----------------------------
        if data.dependents > 0:
            dependent_credit = (Decimal(data.dependents) * Decimal("2000")) / multiplier_dec
            per_period_tax -= dependent_credit

        # -----------------------------
        # 7. Additional withholding (W‑4 Step 4(c))
        # -----------------------------
        per_period_tax += data.additional_withholding

        # Final rounding
        return max(per_period_tax, Decimal("0.00")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    def _apply_brackets(self, income: Decimal, brackets) -> Decimal:
        tax = Decimal("0.00")

        for i in range(len(brackets)):
            threshold, rate = brackets[i]

            # Last bracket
            if i == len(brackets) - 1:
                tax += (income - threshold) * rate
                break

            next_threshold = brackets[i + 1][0]

            if income > threshold:
                taxable_amount = min(income, next_threshold) - threshold
                tax += taxable_amount * rate

        return tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
