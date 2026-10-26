"""
Jurisdiction rules for payroll tax handling.

This module defines:
- State reciprocity agreements
- Functions to determine which state's tax rules apply
- Future expansion for jurisdiction-specific overrides
"""

from typing import Optional


# ---------------------------------------------------------
# Reciprocity agreements
# ---------------------------------------------------------
# Key: work state
# Value: set of states whose residents are exempt from work-state tax
RECIPROCITY = {
    "NJ": {"PA"},   # PA residents working in NJ pay PA tax only
    "PA": {"NJ"},   # NJ residents working in PA pay NJ tax only
}


def get_tax_jurisdiction(work_state: str, home_state: str) -> str:
    """
    Determine which state's tax rules apply based on reciprocity.

    Rules:
    - If home_state is in the reciprocity list for work_state,
      then tax is paid to home_state.
    - Otherwise, tax is paid to work_state.
    """

    work_state = work_state.upper()
    home_state = home_state.upper()

    if work_state in RECIPROCITY:
        exempt_states = RECIPROCITY[work_state]
        if home_state in exempt_states:
            return home_state  # Reciprocity applies

    return work_state  # Default: tax where you work


def has_reciprocity(work_state: str, home_state: str) -> bool:
    """
    Returns True if the employee is exempt from work-state tax
    due to a reciprocity agreement.
    """
    work_state = work_state.upper()
    home_state = home_state.upper()

    return (
        work_state in RECIPROCITY
        and home_state in RECIPROCITY[work_state]
    )
