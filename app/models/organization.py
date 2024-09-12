import re
from datetime import datetime
import requests
from sqlalchemy import (
    Column,
    Float,
    Integer,
    String,
    Boolean,
    Date,
    Enum,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import mapped_column, relationship, validates
from app.models.absract_base import BaseModel


# Define custom Enum types
gender = Enum("male", "female", name="gender")
marital_status = Enum("married", "single", "divorced", "widowed", name="marital_status")
religion = Enum("christian", "muslim", "others", name="religion")
title = Enum("Mr", "Mrs", name="title")
termination_grounds = Enum("retirement","death","indiscipline","resignation")

class Country(Enum):
    pass

class State(Enum):
    pass

class City(Enum):
    pass

def fetch_countries_and_cities():
    host = "https://api.countrystatecity.in/v1"
    # Generate list of countries
    api_url = f"{host}/countries"
    headers = {
        'X-CSCAPI-KEY': 'aWlYdHRud0FZR2g4cFVRWWhIdEg0b0xQZzJGdHN6OEZ0cVViT2VkZg=='
    }
    response = requests.get(api_url, headers=headers)
    countries = response.json()

    for country in countries:
        country_name = country["name"]
        country_iso = country["iso2"]
        Country.__members__[country_name] = Country(country_name)

        # Fetch states for this country
        state_api_url = f"{host}/countries/{country_iso}/states"
        state_response = requests.get(state_api_url, headers=headers)
        states = state_response.json()

        for state in states:
            state_name = state["name"]
            state_iso = state["iso2"]
            State.__members__[state_name] = State(state_name)

            # Fetch cities for this country
            city_api_url = f"{host}/countries/{country_iso}/states/{state_iso}/cities"
            city_response = requests.get(city_api_url, headers=headers)
            city_data = city_response.json()

            for city in city_data:
                city_name = city["name"]
                City.__members__[city_name] = City(city_name)

# fetch_countries_and_cities()

class Organization(BaseModel):
    __tablename__ = 'organization'

    name = Column(String(255), unique=True, nullable=False)
    updated_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    users = relationship('User', back_populates='organization')
    roles = relationship('Role', back_populates='organization')
    job_titles = relationship('JobTitle', back_populates='organization')
    departments = relationship('Department', back_populates='organization')
    salary_grades = relationship('SalaryGrade', back_populates='organization')
    job_levels = relationship('JobLevel', back_populates='organization')
    employment_types = relationship('EmploymentType', back_populates='organization')
    banks = relationship('Bank', back_populates='organization')


class Role(BaseModel):
    __tablename__ = 'role'

    name = Column(String(255), unique=True, nullable=False)
    organization_id = mapped_column(ForeignKey('organization.id'), nullable=False)
    
    # Relationships
    organization = relationship('Organization', back_populates='roles')
    users = relationship('User', back_populates='role')


class JobTitle(BaseModel):
    __tablename__ = 'job_title'

    name = Column(String(255), unique=True, nullable=False)
    supervisor_id = mapped_column(ForeignKey('user.id'))
    organization_id = mapped_column(ForeignKey('organization.id'), nullable=False)

    # Relationships
    supervisor = relationship('User', back_populates='supervisees')
    organization = relationship('Organization', back_populates='job_titles')
    employees = relationship('EmployeeDetail', back_populates='job_title')


class Department(BaseModel):
    __tablename__ = 'department'

    name = Column(String(255), unique=True, nullable=False)
    head_dpt_id = mapped_column(ForeignKey('user.id'))
    organization_id = mapped_column(ForeignKey('organization.id'), nullable=False)

    # Relationships
    head_dpt = relationship('User', back_populates='departments')
    organization = relationship('Organization', back_populates='departments')
    employees = relationship('EmployeeDetail', back_populates='department')


class SalaryGrade(BaseModel):
    __tablename__ = 'salary_grade'

    name = Column(String, unique=True, nullable=False)
    pay = Column(Float, nullable=False)
    organization_id = mapped_column(ForeignKey('organization.id'), nullable=False)

    # Relationships
    job_levels = relationship('JobLevel', back_populates='salary_grade')
    organization = relationship('Organization', back_populates='salary_grades')


class JobLevel(BaseModel):
    __tablename__ = 'job_level'

    name = Column(String(255), unique=True, nullable=False)
    amount_annual_leave = Column(Integer)
    amount_study_leave = Column(Integer)
    amount_casual_leave = Column(Integer)
    amount_maternity_leave = Column(Integer)
    amount_paternity_leave = Column(Integer)
    amount_sick_leave = Column(Integer)
    salary_grade_id = mapped_column(ForeignKey('salary_grade.id'))
    organization_id = mapped_column(ForeignKey('organization.id'), nullable=False)

    # Relationships
    salary_grade = relationship('SalaryGrade', back_populates='job_levels')
    organization = relationship('Organization', back_populates='salary_grades')
    employees = relationship('EmployeeDetail', back_populates='job_level')


class EmploymentType(BaseModel):
    __tablename__ = 'employment_type'

    name = Column(String(255), unique=True, nullable=False)
    organization_id = mapped_column(ForeignKey('organization.id'), nullable=False)

    # Relationships
    organization = relationship('Organization', back_populates='employment_types')
    employees = relationship('EmployeeDetail', back_populates='employment_type')


class Bank(BaseModel):
    __tablename__ = 'bank'

    name = Column(String(255), unique=True, nullable=False)
    organization_id = mapped_column(ForeignKey('organization.id'), nullable=False)

    # Relationships
    organization = relationship('Organization', back_populates='banks')
    employees = relationship('EmployeeDetail', back_populates='bank')

class EmployeeDetail(BaseModel):
    __tablename__ = 'employee_detail'

    user_id = mapped_column(ForeignKey('user.id'), nullable=False)
    employee_number = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(255), nullable=False)
    middle_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    gender = Column(gender, nullable=False)
    marital_status = Column(marital_status, nullable=False)
    d_o_b = Column(Date, nullable=False)
    religion = Column(religion, nullable=False)
    disabled = Column(Boolean, default=False)
    disability_details = Column(String(500))
    title = Column(title)
    # country = Column(Enum(Country))
    # state = Column(Enum(State))
    # city = Column(Enum(City))
    picture_url = Column(String(500))
    phone_number_1 = Column(String, unique=True, nullable=False)
    phone_number_2 = Column(String, unique=True, nullable=False)
    personal_email = Column(String, unique=True, nullable=False)
    job_title_id = mapped_column(ForeignKey('job_title.id'), nullable=False)
    department_id = mapped_column(ForeignKey('department.id'), nullable=False)
    job_level_id = mapped_column(ForeignKey('job_level.id'), nullable=False)
    employment_type_id = mapped_column(ForeignKey('employment_type.id'), nullable=False)
    date_joined = Column(Date, nullable=False)
    date_of_last_promotion = Column(Date)
    date_of_leaving = Column(Date)
    termination_grounds = Column(termination_grounds)
    bank_id = mapped_column(ForeignKey('bank.id'), nullable=False)
    account_number = Column(Integer, unique=True, nullable=False)
    updated_at = Column(DateTime, default=datetime.now)

    # Relationships
    user = relationship('User', back_populates='profile')
    job_title = relationship('JobTitle', back_populates='employees')
    department = relationship('Department', back_populates='employees')
    job_level = relationship('JobLevel', back_populates='employees')
    employment_type = relationship('EmploymentType', back_populates='employees')
    bank = relationship('Bank', back_populates='employees')


    @validates('phone_number_1')
    def validate_phone_number_1(self, key, phone_number):
        pattern = r"^\+\d{1,3}\d{1,14}$"
        if not re.match(pattern, phone_number):
            raise ValueError("Invalid phone number")
    
    @validates('phone_number_2')
    def validate_phone_number_2(self, key, phone_number):
        pattern = r"^\+\d{1,3}\d{1,14}$"
        if not re.match(pattern, phone_number):
            raise ValueError("Invalid phone number")
        if phone_number == self.phone_number_1:
            raise ValueError("Phone number 1 cannot be the same as phone number 2")
    
    @validates('personal_email')
    def validate_email(self, key, email):
        email_regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})+$"
        if not re.match(email_regex, email):
            raise ValueError("Invalid email address")

