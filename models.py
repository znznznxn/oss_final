from sqlalchemy import Column, Integer, String, ForeignKey

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)

class Friends(Base):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True)
    user1_id = Column(String, ForeignKey("users.name"))
    user2_id = Column(String, ForeignKey("users.name"))

class Header(Base):
    __tablename__ = "headers"

    id = Column(Integer, primary_key=True)
    from_id = Column(String, ForeignKey("users.name"))
    to_id = Column(String, ForeignKey("users.name"))