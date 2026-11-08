import os
from backend.app.db import SessionLocal
from backend.app.models import User
from backend.app.security import hash_password
def main():
    db=SessionLocal()
    try:
        if db.query(User).filter(User.role=="admin").count(): raise SystemExit("Admin already exists")
        email=os.environ["ADMIN_EMAIL"].strip().lower()
        name=os.environ.get("ADMIN_NAME","ClinAssist Administrator")
        password=os.environ["ADMIN_PASSWORD"]
        if db.query(User).filter(User.email==email).first(): raise SystemExit("Email already registered")
        db.add(User(email=email,full_name=name,hashed_password=hash_password(password),role="admin"))
        db.commit();print("Admin created:",email)
    finally: db.close()
if __name__=="__main__": main()
