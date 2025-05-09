from sqlalchemy import Boolean, Column, Integer, String, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from enum import Enum

from app.db.base_class import Base

class Role(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(SQLAlchemyEnum(Role), default=Role.USER)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    # Relations
    allocations_created = relationship("Allocation", back_populates="created_by_user", foreign_keys="Allocation.created_by")
    allocations_updated = relationship("Allocation", back_populates="updated_by_user", foreign_keys="Allocation.updated_by")

    def __repr__(self):
        return f"<User {self.email}>" 