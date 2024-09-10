from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import mapped_column, relationship
from app.config.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(150))
    last_name = Column(String(150))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(100))
    is_active = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True, default=None, server_default=None)
    updated_at = Column(DateTime, nullable=True, default=None, server_default=None, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    
    tokens = relationship('UserRefreshToken', back_populates='user')

    def get_context_string(self, context: str):
        return f'{context}{self.password[-6:]}{self.updated_at.strftime("%m%d%Y%H%M%S")}'.strip()


class UserRefreshToken(Base):
    __tablename__ = 'user_refresh_tokens'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(ForeignKey('users.id'))
    refresh_key = Column(String(250), nullable=True, index=True, unique=True)
    expires_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True, default=None, server_default=None, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    user = relationship('User', back_populates='tokens')


class TokenBlacklist(Base):
    __tablename__ = 'token_blacklists'
    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(250), nullable=True, index=True, unique=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    
