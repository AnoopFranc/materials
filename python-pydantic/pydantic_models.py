from typing import Self
from datetime import date
from uuid import UUID, uuid4
from enum import Enum
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)


class Department(Enum):
    HR = "HR"
    SALES = "SALES"
    IT = "IT"
    ENGINEERING = "ENGINEERING"


class Employee(BaseModel):
    employee_id: UUID = Field(default_factory=lambda: uuid4(), frozen=True)
    name: str = Field(min_length=1, frozen=True)
    email: EmailStr = Field(pattern=r".+@company\.com$")
    date_of_birth: date = Field(alias="birth_date", repr=False, frozen=True)
    salary: float = Field(alias="compensation", gt=0, repr=False)
    department: Department
    elected_benefits: bool

    @field_validator("date_of_birth")
    @classmethod
    def check_valid_age(cls, date_of_birth: date) -> date:

        date_delta = date.today() - date_of_birth
        age = date_delta.days / 365

        if age < 18:
            raise ValueError("Employees must be at least 18 years old.")

        return date_of_birth

    @model_validator(mode="after")
    def check_it_benefits(self) -> Self:

        department = self.department
        elected_benefits = self.elected_benefits

        if department == Department.IT and elected_benefits:
            raise ValueError(
                "IT employees are contractors and don't qualify for benefits."
            )
        return self


new_employee = {
    "name": "Chris DeTuma",
    "email": "cdetuma@company.com",
    "birth_date": "1998-04-02",
    "compensation": 100_000,
    "department": "IT",
    "elected_benefits": True,
}
