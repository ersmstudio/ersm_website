from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext

from . import models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="FastAPI + PostgreSQL API 🚀",
    description="واجهة برمجية لإدارة المستخدمين والمحتوى",
    version="1.0.0"
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "🎉 Welcome to FastAPI + PostgreSQL API"}

@app.post("/users/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.UserDB).filter(models.UserDB.email == user.email).first():
        raise HTTPException(status_code=400, detail="❌ Email already registered")

    hashed_pw = get_password_hash(user.password)
    new_user = models.UserDB(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw,
        avatar_url=user.avatar_url
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/", response_model=List[schemas.UserOut], tags=["Users"])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.UserDB).all()

@app.put("/users/{user_id}", response_model=schemas.UserOut, tags=["Users"])
def update_user(user_id: int, data: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.UserDB).filter(models.UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="❌ User not found")

    # تحديث البيانات فقط لو أُرسلت
    if data.username is not None:
        user.username = data.username

    if data.email is not None:
        # التأكد من أن الإيميل الجديد غير مستخدم
        existing_user = db.query(models.UserDB).filter(models.UserDB.email == data.email).first()
        if existing_user and existing_user.id != user.id:
            raise HTTPException(status_code=400, detail="❌ Email already in use by another user")
        user.email = data.email

    if data.avatar_url is not None:
        user.avatar_url = data.avatar_url

    if data.password is not None:
        user.hashed_password = get_password_hash(data.password)

    db.commit()
    db.refresh(user)
    return user


@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserDB).filter(models.UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="❌ User not found")

    db.delete(user)
    db.commit()
    return {"detail": f"✅ User with ID {user_id} deleted successfully"}
