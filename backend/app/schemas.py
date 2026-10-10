from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from .models import Role, Species


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    full_name: str = Field(min_length=1, max_length=120)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    full_name: str
    role: Role


class PetCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    species: Species = Species.dog
    breed: str | None = None
    birth_date: date | None = None
    weight_kg: float | None = Field(default=None, gt=0, lt=200)
    allergies: str | None = None


class PetOut(PetCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    age_years: float | None
    created_at: datetime
     