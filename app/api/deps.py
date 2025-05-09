from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")

def get_db() -> Generator:
    """Dépendance pour obtenir une session de base de données"""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """Dépendance pour obtenir l'utilisateur courant"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les identifiants",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: Optional[int] = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dépendance pour obtenir l'utilisateur courant actif"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Utilisateur inactif")
    return current_user

def get_current_active_superuser(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Dépendance pour obtenir l'utilisateur courant actif et superuser"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, 
            detail="L'utilisateur n'a pas les privilèges suffisants"
        )
    return current_user
