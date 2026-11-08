from datetime import timedelta
from fastapi import HTTPException
from jose import jwt
import pytest
from backend.app.security import hash_password,verify_password,create_access_token,get_current_user
from backend.app.core.config import settings

def test_password_hash():
    h=hash_password("a-long-and-unique-password")
    assert verify_password("a-long-and-unique-password",h)

def test_password_minimum():
    with pytest.raises(ValueError): hash_password("short")

def test_long_password_hash():
    password="long-password-"*12
    assert verify_password(password,hash_password(password))

def test_token_subject():
    assert jwt.decode(create_access_token("42"),settings.secret_key,algorithms=["HS256"])["sub"]=="42"

def test_malformed_non_numeric_subject_returns_401_not_500():
    token=jwt.encode({"sub":"not-an-integer","exp":__import__("datetime").datetime.now(__import__("datetime").timezone.utc)+timedelta(minutes=5)},settings.secret_key,algorithm="HS256")
    with pytest.raises(HTTPException) as exc: get_current_user(token=token,db=object())
    assert exc.value.status_code==401
