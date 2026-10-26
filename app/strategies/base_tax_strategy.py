"""
Base class for all tax strategies.
"""

from abc import ABC, abstractmethod
from decimal import Decimal
from ..core.models import PayInput


class BaseTaxStrategy(ABC):
    """
    Abstract base class for tax calculation strategies.
    All tax strategies must return Decimal for payroll-safe precision.
    """

    @abstractmethod
    def calculate(self, gross_pay: Decimal, data: PayInput) -> Decimal:
        """
        Calculate taxes based on gross pay and input data.
        Must be implemented by subclasses.
        """
        pass
