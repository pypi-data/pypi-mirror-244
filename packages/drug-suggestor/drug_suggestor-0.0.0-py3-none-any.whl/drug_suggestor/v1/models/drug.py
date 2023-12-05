from typing import List

from pydantic import BaseModel, ConfigDict, Field


class Drug(BaseModel):
    """
    Drug model.
    """

    name: str = Field(..., title="Drug name")
    description: str = Field(..., title="Drug description")
    side_effects: str = Field(..., title="Drug side effects")
    contraindications: str = Field(..., title="Drug contraindications")
    dosage: str = Field(..., title="Drug dosage")

    manufacturer: List["Company"]

    model_config = ConfigDict(extra="forbid")


class Company(BaseModel):
    """
    Company model.
    """

    name: str = Field(..., title="Company name")
    description: str = Field(..., title="Company description")
    model_config = ConfigDict(extra="forbid")
