from sqlalchemy.orm import Session

from models import User
from schemas import UserSchema

def db_add_user(db: Session, user: UserSchema):
    db_item = User(name=user.username, password=user.password)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return True