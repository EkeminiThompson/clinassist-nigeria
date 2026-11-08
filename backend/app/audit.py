import json
from sqlalchemy.orm import Session
from backend.app.models import AuditLog,User
def record_event(db:Session,user:User|None,action:str,resource:str,details:dict|None=None):
 event=AuditLog(user_id=user.id if user else None,action=action,resource=resource,details=json.dumps(details or {},sort_keys=True));db.add(event);db.commit();return event
