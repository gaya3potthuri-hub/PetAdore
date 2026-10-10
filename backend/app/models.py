import enum
from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Enum, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def utcnow():
    return datetime.now(timezone.utc)


class Role(str, enum.Enum):
    owner = "owner"
    vet = "vet"
    groomer = "groomer"


class Species(str, enum.Enum):
    dog = "dog"
    cat = "cat"
    other = "other"


class CareKind(str, enum.Enum):
    feeding = "feeding"
    weight = "weight"
    medicine = "medicine"
    exercise = "exercise"
    grooming = "grooming"
    vet_visit = "vet_visit"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))  # never store plain passwords
    full_name: Mapped[str] = mapped_column(String(120))
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.owner)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    pets: Mapped[list["Pet"]] = relationship(back_populates="owner", cascade="all, delete-orphan")


class Pet(Base):
    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(80))
    species: Mapped[Species] = mapped_column(Enum(Species), default=Species.dog)
    breed: Mapped[str | None] = mapped_column(String(80), nullable=True)
    sex: Mapped[str | None] = mapped_column(String(10), nullable=True)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)  # age is computed from this
    weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    allergies: Mapped[str | None] = mapped_column(Text, nullable=True)
    medical_history: Mapped[str | None] = mapped_column(Text, nullable=True)
    food_preferences: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    owner: Mapped[User] = relationship(back_populates="pets")
    vaccinations: Mapped[list["Vaccination"]] = relationship(
        back_populates="pet", cascade="all, delete-orphan"
    )
    care_logs: Mapped[list["CareLog"]] = relationship(
        back_populates="pet", cascade="all, delete-orphan"
    )

    @property
    def age_years(self):
        if not self.birth_date:
            return None
        return round((date.today() - self.birth_date).days / 365.25, 1)


class Vaccination(Base):
    __tablename__ = "vaccinations"

    id: Mapped[int] = mapped_column(primary_key=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    given_on: Mapped[date] = mapped_column(Date)
    next_due_on: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)  # powers reminders later
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    pet: Mapped[Pet] = relationship(back_populates="vaccinations")


class CareLog(Base):
    __tablename__ = "care_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"), index=True)
    kind: Mapped[CareKind] = mapped_column(Enum(CareKind), index=True)
    value: Mapped[float | None] = mapped_column(Float, nullable=True)  # kg, grams, minutes...
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    logged_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)

    pet: Mapped[Pet] = relationship(back_populates="care_logs")