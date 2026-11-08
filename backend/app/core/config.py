from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import model_validator
class Settings(BaseSettings):
    secret_key:str="development-only-change-before-deployment"
    access_token_expire_minutes:int=60
    database_url:str="sqlite:///./clinassist.db"
    cors_origins:str="http://localhost:5173,http://localhost:4173"
    environment:str="development"
    model_config=SettingsConfigDict(env_file=".env",extra="ignore",case_sensitive=False)
    @model_validator(mode="after")
    def validate_production_secrets(self):
        if self.environment.lower()=="production":
            if self.secret_key=="development-only-change-before-deployment" or len(self.secret_key)<32:
                raise ValueError("Production requires a unique SECRET_KEY of at least 32 characters")
            if self.database_url.startswith("sqlite"):
                raise ValueError("Production requires a managed database; SQLite is development-only")
        return self
    @property
    def allowed_origins(self):
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]
settings=Settings()
