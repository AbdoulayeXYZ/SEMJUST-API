from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base_class import Base

class NotificationType(str, enum.Enum):
    ALLOCATION_CREATED = "allocation_created"
    ALLOCATION_UPDATED = "allocation_updated"
    ALLOCATION_DELETED = "allocation_deleted"
    THRESHOLD_ALERT = "threshold_alert"
    SYSTEM_ALERT = "system_alert"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime, nullable=True)
    
    # Relations
    user = relationship("User", back_populates="notifications") 