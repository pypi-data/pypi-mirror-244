from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"


class Patient(BaseModel):
    age: int = Field(..., gt=0, description="Age of the patient")
    gender: GenderEnum
    model_config = ConfigDict(extra="forbid")
