from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlmodel import Session
from pydantic import BaseModel, EmailStr
from app.database import get_session
from app.services import auth_service
from app.utils.security import create_access_token, decode_access_token
from app.models import User

router = APIRouter(prefix='/auth', tags=['Authentication'])


class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post('/register', status_code=201)
def register(body: RegisterRequest, session: Session = Depends(get_session)):
    if auth_service.get_user_by_email(session, body.email):
        raise HTTPException(400, 'Email already registered')
    user = auth_service.create_user(
        session, body.email, body.full_name, body.password
    )
    return {'id': str(user.id), 'email': user.email, 'full_name': user.full_name}


@router.post('/login')
def login(body: LoginRequest, response: Response,
          session: Session = Depends(get_session)):
    user = auth_service.authenticate_user(session, body.email, body.password)
    if not user:
        raise HTTPException(401, 'Invalid email or password')

    token = create_access_token(str(user.id))
    response.set_cookie(
        key='access_token',
        value=token,
        httponly=True,
        secure=False,
        samesite='lax',
        max_age=3600,
    )
    return {'id': str(user.id), 'email': user.email, 'full_name': user.full_name}


@router.post('/logout')
def logout(response: Response):
    response.delete_cookie('access_token')
    return {'message': 'Logged out'}


def get_current_user(access_token: str = Cookie(None),
                      session: Session = Depends(get_session)) -> User:
    if not access_token:
        raise HTTPException(401, 'Not authenticated')
    payload = decode_access_token(access_token)
    user = session.get(User, payload.get('sub'))
    if not user or not user.is_active:
        raise HTTPException(401, 'User not found or inactive')
    return user


@router.get('/me')
def get_me(current_user: User = Depends(get_current_user)):
    return {
        'id': str(current_user.id),
        'email': current_user.email,
        'full_name': current_user.full_name,
    }