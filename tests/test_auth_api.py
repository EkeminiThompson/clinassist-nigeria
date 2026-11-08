from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.app.main import app
from backend.app.db import Base,get_db

def test_registration_is_least_privilege_and_login_works():
    engine=create_engine("sqlite://",connect_args={"check_same_thread":False},poolclass=StaticPool)
    Base.metadata.create_all(engine);Session=sessionmaker(bind=engine,autoflush=False)
    def override_db():
        db=Session()
        try: yield db
        finally: db.close()
    app.dependency_overrides[get_db]=override_db
    client=TestClient(app)
    payload={"email":"viewer@example.org","full_name":"Test Viewer","password":"a-secure-test-password","role":"admin"}
    registered=client.post("/api/v1/auth/register",json=payload)
    assert registered.status_code==201 and registered.json()["role"]=="viewer"
    login=client.post("/api/v1/auth/login",data={"username":"viewer@example.org","password":payload["password"]})
    assert login.status_code==200
    token=login.json()["access_token"]
    headers={"Authorization":f"Bearer {token}"}
    assert client.get("/api/v1/auth/me",headers=headers).json()["role"]=="viewer"
    assert client.get("/api/v1/auth/users",headers=headers).status_code==403
    app.dependency_overrides.clear();Base.metadata.drop_all(engine);engine.dispose()
