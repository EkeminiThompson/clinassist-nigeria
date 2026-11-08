from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel,EmailStr,Field
from sqlalchemy.orm import Session
from backend.app.audit import record_event
from backend.app.db import get_db
from backend.app.models import User
from backend.app.security import create_access_token,get_current_user,hash_password,verify_password,require_roles
router=APIRouter(prefix='/api/v1/auth',tags=['authentication'])
class Register(BaseModel): email:EmailStr;full_name:str=Field(min_length=2,max_length=160);password:str=Field(min_length=12,max_length=128)
class UserOut(BaseModel):
 id:int;email:EmailStr;full_name:str;role:str;is_active:bool
 model_config={'from_attributes':True}
@router.post('/register',response_model=UserOut,status_code=201)
def register(p:Register,db:Session=Depends(get_db)):
 email=str(p.email).lower()
 if db.query(User).filter(User.email==email).first(): raise HTTPException(409,'Account already exists')
 u=User(email=email,full_name=p.full_name.strip(),hashed_password=hash_password(p.password),role='clinician');db.add(u);db.commit();db.refresh(u);record_event(db,u,'account.registered','user');return u
@router.post('/login')
def login(form:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
 u=db.query(User).filter(User.email==form.username.lower()).first()
 if not u or not u.is_active or not verify_password(form.password,u.hashed_password): raise HTTPException(401,'Incorrect email or password')
 record_event(db,u,'auth.login','session');return {'access_token':create_access_token(u.id),'token_type':'bearer','user':UserOut.model_validate(u).model_dump()}
@router.get('/me',response_model=UserOut)
def me(u:User=Depends(get_current_user)): return u
@router.get('/users',response_model=list[UserOut])
def users(db:Session=Depends(get_db),admin:User=Depends(require_roles('admin'))):
 record_event(db,admin,'admin.users.list','user');return db.query(User).all()
@router.patch('/users/{user_id}/role',response_model=UserOut)
def role(user_id:int,role:str,db:Session=Depends(get_db),admin:User=Depends(require_roles('admin'))):
 if role not in {'admin','clinician','researcher','viewer'}: raise HTTPException(422,'Unsupported role')
 target=db.query(User).filter(User.id==user_id).first()
 if not target: raise HTTPException(404,'User not found')
 if target.id==admin.id and role!='admin': raise HTTPException(400,'Cannot demote yourself')
 target.role=role;db.commit();db.refresh(target);record_event(db,admin,'admin.role.changed',f'user:{target.id}',{'role':role});return target
