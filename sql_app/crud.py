from sqlalchemy.orm import Session

from . import models, schemas

from pydantic import parse_obj_as

def get_user(db: Session, user_id: int):
    return schemas.User.from_orm(db.query(models.User).filter(models.User.id == user_id).first())

def get_user_by_email(db:Session, email: str):
    return schemas.User.from_orm(db.query(models.User).filter(models.User.email == email).first())

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return parse_obj_as(schemas.List[schemas.User], db.query(models.User).offset(skip).limit(limit).all())

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashes_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashes_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return schemas.User.from_orm(db_user)

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return parse_obj_as(schemas.List[schemas.Item], db.query(models.Item).offset(skip).limit(limit).all())

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return schemas.Item.from_orm(db_item)

