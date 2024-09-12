import uuid
from sqlalchemy import Column, DateTime, func, text, Uuid
from app.config.database import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Uuid, primary_key=True, unique=True, default=uuid.uuid4, server_default=text('uuid_generate_v4()'))
    created_at = Column(DateTime, nullable=False, server_default=func.now())


