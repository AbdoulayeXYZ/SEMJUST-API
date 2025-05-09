from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.notification import Notification, NotificationType
from app.schemas.notification import NotificationCreate
from app.core.config import settings
from app.utils.email import send_email

class NotificationService:
    @staticmethod
    def create_notification(
        db: Session,
        *,
        user_id: int,
        type: NotificationType,
        title: str,
        message: str,
        send_email_notification: bool = True
    ) -> Notification:
        """
        Crée une nouvelle notification et l'envoie par email si demandé.
        """
        notification = Notification(
            user_id=user_id,
            type=type,
            title=title,
            message=message
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)

        if send_email_notification:
            # Envoyer l'email de notification
            send_email(
                email_to=notification.user.email,
                subject=title,
                html_content=message
            )

        return notification

    @staticmethod
    def get_user_notifications(
        db: Session,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        unread_only: bool = False
    ) -> List[Notification]:
        """
        Récupère les notifications d'un utilisateur.
        """
        query = db.query(Notification).filter(Notification.user_id == user_id)
        
        if unread_only:
            query = query.filter(Notification.is_read == False)
            
        return query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def mark_as_read(
        db: Session,
        *,
        notification_id: int,
        user_id: int
    ) -> Optional[Notification]:
        """
        Marque une notification comme lue.
        """
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()
        
        if notification:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
            db.commit()
            db.refresh(notification)
            
        return notification

    @staticmethod
    def mark_all_as_read(
        db: Session,
        *,
        user_id: int
    ) -> int:
        """
        Marque toutes les notifications d'un utilisateur comme lues.
        Retourne le nombre de notifications mises à jour.
        """
        result = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).update({
            "is_read": True,
            "read_at": datetime.utcnow()
        })
        
        db.commit()
        return result

    @staticmethod
    def delete_notification(
        db: Session,
        *,
        notification_id: int,
        user_id: int
    ) -> Optional[Notification]:
        """
        Supprime une notification.
        """
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()
        
        if notification:
            db.delete(notification)
            db.commit()
            
        return notification 