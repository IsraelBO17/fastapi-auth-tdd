import re
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import mapped_column, relationship, validates
from app.models.absract_base import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    username = Column(String(255), unique=True, nullable=False)
    organization_email = Column(String, unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role_id = mapped_column(ForeignKey('role.id'), nullable=False)
    organization_id = mapped_column(ForeignKey('organization.id'), nullable=False)
    is_active = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.now)

    # Relationships
    role = relationship('Role', back_populates='users')
    profile = relationship('EmployeeDetail', uselist=False, back_populates='user')
    organization = relationship('Organization', back_populates='users')
    supervisees = relationship('JobTitle', back_populates='supervisor')
    departments = relationship('Department', uselist=False, back_populates='head_dpt')
    tokens = relationship('UserRefreshToken', back_populates='user')

    @validates('organization_email')
    def validate_email(self, key, email):
        email_regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})+$"
        if not re.match(email_regex, email):
            raise ValueError("Invalid email address")

    def get_context_string(self, context: str):
        return f'{context}{self.password[-6:]}{self.updated_at.strftime("%m%d%Y%H%M%S")}'.strip()


class UserRefreshToken(BaseModel):
    __tablename__ = 'user_refresh_tokens'

    user_id = mapped_column(ForeignKey('user.id'), nullable=False)
    refresh_key = Column(String(250), nullable=False, index=True, unique=True)
    expires_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True, default=None, server_default=None, onupdate=datetime.now)

    user = relationship('User', back_populates='tokens')


class TokenBlacklist(BaseModel):
    __tablename__ = 'token_blacklists'

    token = Column(String(250), nullable=False, index=True, unique=True)
    
