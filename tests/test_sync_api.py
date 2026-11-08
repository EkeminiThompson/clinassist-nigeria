from datetime import datetime,timezone
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.app.main import app
from backend.app.db import Base,get_db
from backend.app.models import User,SyncReceipt
from backend.app.security import hash_password,create_access_token

def test_sync_is_idempotent_and_rejects_clinical_payload():
    engine=create_engine("sqlite://",connect_args={"check_same_thread":False},poolclass=StaticPool)
    Base.metadata.create_all(engine);Session=sessionmaker(bind=engine,autoflush=False)
    def override_db():
        db=Session()
        try: yield db
        finally: db.close()
    app.dependency_overrides[get_db]=override_db
    db=Session();user=User(email="sync-test@example.org",full_name="Sync Test",hashed_password=hash_password("test-password-long"));db.add(user);db.commit();db.refresh(user);uid=user.id;db.close()
    token=create_access_token(uid);client=TestClient(app);headers={"Authorization":f"Bearer {token}"}
    body={"records":[{"client_id":"offline_12345678","record_type":"prediction","created_at":datetime.now(timezone.utc).isoformat()}]}
    first=client.post("/api/v1/sync/batch",json=body,headers=headers)
    second=client.post("/api/v1/sync/batch",json=body,headers=headers)
    assert first.status_code==200 and first.json()["accepted"]==1
    assert second.status_code==200 and second.json()["accepted"]==0 and second.json()["duplicate_count"]==1
    bad={"records":[{**body["records"][0],"payload":{"Glucose":999}}]}
    assert client.post("/api/v1/sync/batch",json=bad,headers=headers).status_code==422
    db=Session();assert db.query(SyncReceipt).filter_by(user_id=uid).count()==1;db.close()
    app.dependency_overrides.clear();Base.metadata.drop_all(engine);engine.dispose()
