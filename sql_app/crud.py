from sqlalchemy.orm import Session

from . import models, schemas

from pydantic import parse_obj_as

# id is primary key
def get_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return None
    return db_user
    # return db.query(models.User).filter(models.User.id == user_id).first()

# email is unique key
def get_user_by_email(db:Session, email: str):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user is None:
        return None
    return schemas.User.from_orm(db_user)
    # return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    # TODO: do hashing.
    fake_hashes_password = user.password + "notreallyhashed"
    # Generates SQLAlchemy model instance
    db_user = models.User(email=user.email, hashed_password=fake_hashes_password)
    # Add instance to DB
    db.add(db_user)
    # Commit (after finishes, irreversible)
    db.commit()
    # New data immediately appears when fetch.
    db.refresh(db_user)
    return db_user

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

