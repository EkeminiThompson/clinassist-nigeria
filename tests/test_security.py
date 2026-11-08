from backend.app.security import hash_password,verify_password,create_access_token
from jose import jwt
from backend.app.core.config import settings
def test_password_hash():
 h=hash_password('a-long-and-unique-password');assert verify_password('a-long-and-unique-password',h)
def test_password_minimum():
 try:hash_password('short')
 except ValueError:return
 assert False
def test_token_subject():assert jwt.decode(create_access_token('42'),settings.secret_key,algorithms=['HS256'])['sub']=='42'
