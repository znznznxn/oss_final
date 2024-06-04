from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    username: Optional[str]
    password: Optional[str]

    class Config:
        orm_mode = True