from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError

from app.core.config import settings


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


def hash_password(password: str) -> str:
    """Хешировать пароль с помощью argon2"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверить пароль на соответствие хешу"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """Создать JWT токен с данными и временем истечения"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret, algorithm=ALGORITHM)
    return encoded_jwt


def access_token(username: str) -> dict:
    """Получение токена для пользователя"""
    return {
        "access_token": create_access_token(data={"sub": username}),
    }


def decode_access_token(token: str) -> int | None:
    """Декодировать JWT токен и получить данные."""
    if token is None:
        return None
    try:
        payload = jwt.decode(token, settings.secret, algorithms=[ALGORITHM])
        return int(payload.get("sub"))
    except (JWTError, ValueError, TypeError):
        return None
