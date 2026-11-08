from datetime import datetime,timedelta,timezone
from jose import JWTError,jwt
from passlib.context import CryptContext
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.app.core.config import settings
from backend.app.db import get_db
from backend.app.models import User
pwd_context=CryptContext(schemes=["argon2"],deprecated="auto")
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
def hash_password(password:str)->str:
    if len(password)<12: raise ValueError("Password must contain at least 12 characters")
    return pwd_context.hash(password)
def verify_password(password:str,hashed_password:str)->bool:
    try: return bool(pwd_context.verify(password,hashed_password))
    except Exception: return False
def create_access_token(subject):
    now=datetime.now(timezone.utc)
    return jwt.encode({"sub":str(subject),"iat":now,"exp":now+timedelta(minutes=settings.access_token_expire_minutes)},settings.secret_key,algorithm="HS256")
def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    error=HTTPException(status_code=401,detail="Invalid or expired credentials",headers={"WWW-Authenticate":"Bearer"})
    try:
        payload=jwt.decode(token,settings.secret_key,algorithms=["HS256"])
        subject=payload.get("sub")
        if not subject: raise error
        user_id=int(subject)
    except (JWTError,TypeError,ValueError): raise error
    user=db.query(User).filter(User.id==user_id,User.is_active.is_(True)).first()
    if user is None: raise error
    return user
def require_roles(*roles):
    def check(user:User=Depends(get_current_user)):
        if user.role not in roles: raise HTTPException(403,"Insufficient permissions")
        return user
    return check
