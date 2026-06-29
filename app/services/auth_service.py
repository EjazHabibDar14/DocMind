from sqlmodel import Session, select
from app.models import User
from app.utils.security import hash_password, verify_password


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.exec(
        select(User).where(User.email == email)
    ).first()


def create_user(session: Session, email: str, full_name: str, password: str) -> User:
    user = User(
        email=email,
        full_name=full_name,
        hashed_password=hash_password(password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate_user(session: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user