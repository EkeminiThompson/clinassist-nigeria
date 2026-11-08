from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
 secret_key:str='CHANGE-ME-before-deployment'
 access_token_expire_minutes:int=60
 database_url:str='sqlite:///./clinassist.db'
 cors_origins:str='http://localhost:5173,http://localhost:4173'
 model_config=SettingsConfigDict(env_file='.env',extra='ignore')
 @property
 def allowed_origins(self): return [x.strip() for x in self.cors_origins.split(',') if x.strip()]
settings=Settings()
