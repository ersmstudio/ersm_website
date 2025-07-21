from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from .database import Base, engine, SessionLocal
from sqlalchemy import Column, Integer, String

# ---------- Database Models ----------

class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

# Create tables in DB
Base.metadata.create_all(bind=engine)

# ---------- Pydantic Schemas ----------

class UserCreate(BaseModel):
    name: str
    email: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

# ---------- FastAPI App ----------

app = FastAPI(title="FastAPI + PostgreSQL API")

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Routes ----------

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to FastAPI + PostgreSQL API"}

@app.post("/users/", response_model=UserOut, tags=["Users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = UserDB(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/", response_model=List[UserOut], tags=["Users"])
def list_users(db: Session = Depends(get_db)):
    return db.query(UserDB).all()
