from typing import Any

from sqlalchemy.orm import Session

from src.presentation.fastapi import models, schemas


def get_users(db: Session, skip: int = 0, limit: int = 100) -> Any:
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int) -> Any:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Any:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    fake_hashed_password = hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=fake_hashed_password,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        gender=user.gender,
        country=user.country,
        isActive=user.isActive,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: schemas.UserCreate) -> Any:
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        return None
    for field in user.__dict__:
        setattr(db_user, field, getattr(user, field))
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> Any:
    record_obj = db.query(models.User).filter(models.User.id == user_id).first()
    if not record_obj:
        return None
    db.delete(record_obj)
    db.commit()
    return record_obj
