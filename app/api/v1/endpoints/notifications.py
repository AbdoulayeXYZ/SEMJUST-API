from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import schemas
from app.models.user import User
from app.api import deps
from app.services.notification_service import NotificationService

router = APIRouter()

@router.get("/", response_model=List[schemas.Notification])
def read_notifications(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    unread_only: bool = False,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Récupère les notifications de l'utilisateur courant.
    """
    notifications = NotificationService.get_user_notifications(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        unread_only=unread_only
    )
    return notifications

@router.post("/{notification_id}/read", response_model=schemas.Notification)
def mark_notification_as_read(
    *,
    db: Session = Depends(deps.get_db),
    notification_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Marque une notification comme lue.
    """
    notification = NotificationService.mark_as_read(
        db=db,
        notification_id=notification_id,
        user_id=current_user.id
    )
    if not notification:
        raise HTTPException(status_code=404, detail="Notification non trouvée")
    return notification

@router.post("/read-all", response_model=int)
def mark_all_notifications_as_read(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Marque toutes les notifications de l'utilisateur comme lues.
    """
    count = NotificationService.mark_all_as_read(
        db=db,
        user_id=current_user.id
    )
    return count

@router.delete("/{notification_id}", response_model=schemas.Notification)
def delete_notification(
    *,
    db: Session = Depends(deps.get_db),
    notification_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Supprime une notification.
    """
    notification = NotificationService.delete_notification(
        db=db,
        notification_id=notification_id,
        user_id=current_user.id
    )
    if not notification:
        raise HTTPException(status_code=404, detail="Notification non trouvée")
    return notification 