from fastapi import APIRouter,Depends
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from backend.app.audit import record_event
from backend.app.db import get_db
from backend.app.models import User
from backend.app.security import get_current_user
router=APIRouter(prefix='/api/v1/sync',tags=['offline-sync'])
class Record(BaseModel): client_id:str=Field(min_length=8,max_length=80);record_type:str=Field(pattern='^prediction$');created_at:str;payload:dict
class Batch(BaseModel): records:list[Record]=Field(max_length=50)
@router.post('/batch')
def sync(b:Batch,db:Session=Depends(get_db),u:User=Depends(get_current_user)):
 ids=[r.client_id for r in b.records];record_event(db,u,'offline.sync.received','sync_batch',{'count':len(ids),'client_ids':ids})
 return {'accepted':len(ids),'acknowledged_client_ids':ids,'note':'Receipt metadata only; no clinical payload persisted.'}
