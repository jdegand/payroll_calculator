from pydantic import BaseModel, Field, validator
from typing import Optional, List, Literal
from decimal import Decimal


class PayInput(BaseModel):
    # Basic employee + pay info
    employee_id: str
    hours_worked: Decimal
    pay_rate: Decimal

    # Jurisdiction
    work_state: str
    home_state: str

    # Federal tax realism
    filing_status: Literal["single", "married"] = "single"
    pay_frequency: Literal["weekly", "biweekly", "semimonthly", "monthly"] = "weekly"

    # W‑4 Step 3: dependents reduce withholding
    dependents: int = 0

    # W‑4 Step 4(c): extra withholding per paycheck
    additional_withholding: Decimal = Decimal("0.00")

    # Pre‑tax deductions (reduce taxable wages)
    pretax_401k_rate: Optional[Decimal] = None   # e.g., Decimal("0.05") for 5%
    hsa_amount: Optional[Decimal] = None         # fixed amount per paycheck
    fsa_amount: Optional[Decimal] = None         # fixed amount per paycheck

    # Year‑to‑date income (optional but realistic)
    ytd_income: Decimal = Decimal("0.00")

    # Optional post‑tax deductions
    union_dues: Optional[Decimal] = None
    voluntary_deductions: Optional[List[Decimal]] = None

    # Optional garnishments
    child_support_amount: Optional[Decimal] = None
    child_support_rate: Optional[Decimal] = None
    tax_levy_amount: Optional[Decimal] = None
    creditor_garnishment_rate: Optional[Decimal] = None

    # Convert all floats to Decimal automatically
    @validator(
        "hours_worked",
        "pay_rate",
        "additional_withholding",
        "pretax_401k_rate",
        "hsa_amount",
        "fsa_amount",
        "ytd_income",
        "union_dues",
        "child_support_amount",
        "tax_levy_amount",
        "child_support_rate",
        "creditor_garnishment_rate",
        pre=True,
        always=True,
    )
    def convert_to_decimal(cls, v):
        if v is None:
            return v
        return Decimal(str(v))


class PayResult(BaseModel):
    gross_pay: Decimal
    net_pay: Decimal
    taxes: Decimal
    deductions: Decimal
    garnishments: Decimal

    # Ensure all outputs are Decimal
    @validator("*", pre=True)
    def convert_output(cls, v):
        return Decimal(str(v))
