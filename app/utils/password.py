from itsdangerous import URLSafeTimedSerializer
from app.core.config import settings

def generate_password_reset_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(email, salt="password-reset-salt")

def verify_password_reset_token(token: str, expiration: int = 3600) -> str | None:
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        email = serializer.loads(token, salt="password-reset-salt", max_age=expiration)
    except Exception:
        return None
    return email 