from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from app.models.notification import NotificationType

class NotificationBase(BaseModel):
    type: NotificationType
    title: str
    message: str

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationUpdate(BaseModel):
    is_read: bool = True

class NotificationInDBBase(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    created_at: datetime
    read_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class Notification(NotificationInDBBase):
    pass

class NotificationInDB(NotificationInDBBase):
    pass 