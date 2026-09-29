"""Shared state passed between workflow nodes."""

from pydantic import BaseModel, Field

from src.models import Lead, NormalizedMessage


class GraphState(BaseModel):
    """
    Shared state used by the local workflow.

    The initial state contains:
    - the normalized message
    - the captured lead
    - validation errors
    """

    message: NormalizedMessage
    lead: Lead | None = None
    errors: list[str] = Field(default_factory=list)