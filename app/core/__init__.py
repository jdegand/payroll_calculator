"""
Core payroll engine package.

This package contains:
- Data models (Pydantic)
- Payroll engine logic
- Validation utilities
- Jurisdiction rules
"""

from .models import PayInput, PayResult
from .payroll_engine import run_payroll
