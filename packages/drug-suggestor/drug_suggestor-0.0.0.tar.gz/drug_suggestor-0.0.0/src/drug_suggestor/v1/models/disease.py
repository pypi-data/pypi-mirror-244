from pydantic import BaseModel, ConfigDict, Field


class Symptom(BaseModel):
    name: str
    severity: int = Field(..., ge=0, le=10, description="Severity of the symptom")
    model_config = ConfigDict(extra="forbid")
