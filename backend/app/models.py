from datetime import datetime,timezone
from sqlalchemy import Boolean,DateTime,ForeignKey,Integer,String,Text,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column,relationship
from backend.app.db import Base
class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    email:Mapped[str]=mapped_column(String(320),unique=True,index=True)
    full_name:Mapped[str]=mapped_column(String(160))
    hashed_password:Mapped[str]=mapped_column(String(255))
    role:Mapped[str]=mapped_column(String(32),default="clinician")
    is_active:Mapped[bool]=mapped_column(Boolean,default=True)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
    audit_events=relationship("AuditLog",back_populates="user")
class AuditLog(Base):
    __tablename__="audit_logs"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id:Mapped[int|None]=mapped_column(ForeignKey("users.id"),nullable=True,index=True)
    action:Mapped[str]=mapped_column(String(80),index=True)
    resource:Mapped[str]=mapped_column(String(120))
    details:Mapped[str]=mapped_column(Text,default="{}")
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),index=True)
    user=relationship("User",back_populates="audit_events")
class SyncReceipt(Base):
    __tablename__="sync_receipts"
    __table_args__=(UniqueConstraint("user_id","client_id",name="uq_sync_receipt_user_client"),)
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),nullable=False,index=True)
    client_id:Mapped[str]=mapped_column(String(80),nullable=False)
    record_type:Mapped[str]=mapped_column(String(32),nullable=False)
    client_created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False)
    received_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),nullable=False)
