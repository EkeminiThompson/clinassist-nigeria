import pytest
from pydantic import ValidationError
from backend.app.core.config import Settings

def test_production_rejects_default_secret():
    with pytest.raises(ValidationError):
        Settings(environment="production",database_url="postgresql+psycopg://user:pass@localhost/db")

def test_production_rejects_sqlite():
    with pytest.raises(ValidationError):
        Settings(environment="production",secret_key="x"*48,database_url="sqlite:///prod.db")

def test_production_rejects_wildcard_cors():
    with pytest.raises(ValidationError):
        Settings(environment="production",secret_key="x"*48,database_url="postgresql+psycopg://user:pass@localhost/db",cors_origins="*")

def test_production_accepts_explicit_secure_settings():
    cfg=Settings(environment="production",secret_key="x"*48,database_url="postgresql+psycopg://user:pass@localhost/db",cors_origins="https://clinic.example.org",rate_limit_storage_uri="redis://localhost:6379/0")
    assert cfg.allowed_origins==["https://clinic.example.org"]

def test_production_rejects_memory_rate_limit_storage():
    with pytest.raises(ValidationError):
        Settings(environment="production",secret_key="x"*48,
            database_url="postgresql+psycopg://user:pass@localhost/db",
            cors_origins="https://clinic.example.org",rate_limit_storage_uri="memory://")
