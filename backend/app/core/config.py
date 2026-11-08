from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import Field,model_validator
class Settings(BaseSettings):
    secret_key:str="development-only-change-before-deployment"
    access_token_expire_minutes:int=Field(default=60,gt=0,le=1440)
    database_url:str="sqlite:///./clinassist.db"
    cors_origins:str="http://localhost:5173,http://localhost:4173"
    environment:str="development"
    rate_limit_storage_uri:str="memory://"
    model_config=SettingsConfigDict(env_file=".env",extra="ignore",case_sensitive=False)
    @model_validator(mode="after")
    def validate_production_secrets(self):
        if self.environment.lower()=="production":
            if self.secret_key=="development-only-change-before-deployment" or len(self.secret_key)<32:
                raise ValueError("Production requires a unique SECRET_KEY of at least 32 characters")
            if self.database_url.startswith("sqlite"):
                raise ValueError("Production requires a managed database; SQLite is development-only")
            if "*" in self.allowed_origins:
                raise ValueError("Wildcard CORS origins are not allowed in production")
            if not self.rate_limit_storage_uri.startswith(("redis://","rediss://")):
                raise ValueError("Production requires shared Redis-backed rate-limit storage")
        return self
    @property
    def allowed_origins(self):
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]
settings=Settings()
