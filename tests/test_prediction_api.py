from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.app.main import app
from backend.app.db import Base,get_db
from backend.app.models import User
from backend.app.security import hash_password,create_access_token
from backend.app.core.config import settings

def test_production_prediction_endpoint_is_disabled(monkeypatch):
    engine=create_engine("sqlite://",connect_args={"check_same_thread":False},poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Session=sessionmaker(bind=engine,autoflush=False)
    def override_db():
        db=Session()
        try: yield db
        finally: db.close()
    app.dependency_overrides[get_db]=override_db
    db=Session()
    user=User(email="clinician-production@example.org",full_name="Clinician",hashed_password=hash_password("test-password-long"),role="clinician")
    db.add(user);db.commit();db.refresh(user);token=create_access_token(user.id);db.close()
    monkeypatch.setattr(settings,"environment","production")
    client=TestClient(app)
    payload={"features":{"Pregnancies":1,"Glucose":100,"BloodPressure":70,"SkinThickness":20,"Insulin":80,"BMI":25,"DiabetesPedigreeFunction":0.4,"Age":35}}
    response=client.post("/api/v1/predict",json=payload,headers={"Authorization":f"Bearer {token}"})
    assert response.status_code==503
    assert "not completed Nigerian external validation" in response.json()["detail"]
    monkeypatch.setattr(settings,"environment","development")
    app.dependency_overrides.clear();Base.metadata.drop_all(engine);engine.dispose()
