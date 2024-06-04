from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from models import User, Friends
from schemas import UserSchema, FriendSchema

def db_add_user(db: Session, user: UserSchema):
    db_item = User(name=user.username, password=user.password)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return True

def db_add_friend(db: Session, user1: str, user2: str):
    if(db.query(Friends).filter(or_(and_(Friends.user1_id == user1, Friends.user2_id == user2), and_(Friends.user1_id == user2, Friends.user2_id == user1))).first()):
        return False
    db_item = Friends(user1_id=user1, user2_id=user2)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return True

def db_get_friends(db: Session, user: str):
    return db.query(Friends).filter(or_(Friends.user1_id == user,Friends.user2_id == user)).all()
