"""
Factory for selecting the correct tax strategy based on jurisdiction.
"""

from .federal_tax import FederalTaxStrategy
from .state.pa_tax import PennsylvaniaTaxStrategy
from .state.nj_tax import NewJerseyTaxStrategy
from ..core.jurisdiction_rules import get_tax_jurisdiction


# Map state codes to strategy classes
STATE_STRATEGIES = {
    "PA": PennsylvaniaTaxStrategy,
    "NJ": NewJerseyTaxStrategy,
}

def get_tax_strategy(work_state: str, home_state: str = None):
    """
    Determine the correct tax strategy using jurisdiction rules.

    - Applies reciprocity (PA ↔ NJ)
    - Falls back to work_state if no reciprocity
    - Always applies federal tax separately (engine handles combining)
    """

    # Determine which state’s tax rules apply
    tax_state = get_tax_jurisdiction(work_state, home_state or work_state)

    # Get state strategy (default: no state tax)
    state_strategy_cls = STATE_STRATEGIES.get(tax_state)

    if state_strategy_cls:
        return state_strategy_cls()

    # If no state strategy exists, return a no-op strategy
    class NoStateTaxStrategy:
        def calculate(self, gross_pay, data):
            return 0.0

    return NoStateTaxStrategy()
