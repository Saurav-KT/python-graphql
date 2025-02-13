from sqlmodel import Field, MetaData, SQLModel, Relationship
from typing import List, Optional


class BaseModel(SQLModel):
    metadata = MetaData(schema="gql_test")
    SQLModel.metadata = metadata


class Employer(BaseModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False, title="employer name")
    contact_email: str | None = Field(default=None, title="employer contact email ", max_length=200)
    industry: str = Field(nullable=False, title="employer industry")
    jobs: List["Job"] = Relationship(back_populates="employer")


class Job(BaseModel, table=True):
    id: int = Field(primary_key=True)
    title: str = Field(nullable=False, title="job title")
    description: str = Field(nullable=False, title="job description")
    employer_id: int = Field(title="employer table foreign key field", foreign_key="employer.id")
    employer: Optional["Employer"] = Relationship(back_populates="jobs")
    applications: Optional["JobApplication"] = Relationship(back_populates="job")


class User(BaseModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(nullable=False, title="user name")
    email: str = Field(nullable=False, title="user email")
    password_hash: str= Field(nullable=False, title="user password")
    role: str = Field(nullable=False, title="user role")
    applications: Optional["JobApplication"] = Relationship(back_populates="user")


class JobApplication(BaseModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(title="user table foreign key field", foreign_key="user.id")
    job_id: int = Field(title="job table foreign key field", foreign_key="job.id")
    user: Optional["User"] = Relationship(back_populates="applications")
    job: Optional["Job"] = Relationship(back_populates="applications")
