from datetime import datetime
from typing import Literal
from fastapi import APIRouter,Depends
from pydantic import BaseModel,ConfigDict,Field
from sqlalchemy.orm import Session
from backend.app.audit import record_event
from backend.app.db import get_db
from backend.app.models import User,SyncReceipt
from backend.app.security import get_current_user
router=APIRouter(prefix="/api/v1/sync",tags=["offline-sync"])
class Record(BaseModel):
    client_id:str=Field(min_length=8,max_length=80,pattern=r"^[A-Za-z0-9_-]+$")
    record_type:Literal["prediction"]
    created_at:datetime
class Batch(BaseModel):
    records:list[Record]=Field(max_length=50)
@router.post("/batch")
def sync(batch:Batch,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    acknowledged=[];new_ids=[];duplicates=[]
    seen=set()
    for record in batch.records:
        client_id=record.client_id
        if client_id in seen:
            duplicates.append(client_id);continue
        seen.add(client_id)
        exists=db.query(SyncReceipt).filter_by(user_id=user.id,client_id=client_id).first()
        if exists:
            duplicates.append(client_id)
        else:
            db.add(SyncReceipt(user_id=user.id,client_id=client_id,record_type=record.record_type,client_created_at=record.created_at))
            new_ids.append(client_id)
        acknowledged.append(client_id)
    db.commit()
    record_event(db,user,"offline.sync.received","sync_batch",{"accepted":len(new_ids),"duplicates":len(duplicates)})
    return {"accepted":len(new_ids),"duplicate_count":len(duplicates),"acknowledged_client_ids":acknowledged,
            "note":"Only opaque receipt metadata is stored; clinical payloads are not accepted."}
