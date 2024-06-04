from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    username: Optional[str]
    password: Optional[str]

    class Config:
        orm_mode = True

class FriendSchema(BaseModel):
    user1: Optional[str]
    user2: Optional[str]

    class Config:
        orm_mode = True

class HeaderSchema(BaseModel):
    from_id: Optional[str]
    to_id: Optional[str]

    class Config:
        orm_mode = True

class ChatSchema(BaseModel):
    sender_name: Optional[str]
    receiver_name: Optional[str]
    header_id: Optional[int]
    content: Optional[str]
    sent_at: Optional[str]

    class Config:
        orm_mode = True