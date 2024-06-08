from fastapi import FastAPI, Depends, Response, Request, WebSocket
from fastapi.responses import FileResponse, RedirectResponse

from sqlalchemy import or_
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

from models import Base, User, Header
from schema import UserSchema, FriendSchema, HeaderSchema, ChatSchema, LastchatSchema
from database import SessionLocal ,engine
from crud import db_add_user, db_add_friend, db_get_friends, db_get_room, db_get_chatlist, db_add_chat

#O
app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class NotAuthenticatedException(Exception):
    pass
# O , 여기 옵션 잘못 설정되어 있어서 수정함
SECRET = "oss"
manager = LoginManager(SECRET, '/login', use_cookie=True, custom_exception=NotAuthenticatedException)

# O
@app.post('/token')
def login(response: Response, data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password

    user = get_user(username)
    if not user:
        raise InvalidCredentialsException
    if user.password != password:
        raise InvalidCredentialsException
    access_token = manager.create_access_token(
        data={'sub': username}
    )
    manager.set_cookie(response, access_token)
    return {'access_token': access_token}

# O
@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    return RedirectResponse('/login')
# O
@manager.user_loader()
def get_user(username: str, db: Session = None):
    if not db:
        with SessionLocal() as db:
            return db.query(User).filter(User.name == username).first()
    return db.query(User).filter(User.name == username).first()

# O
@app.get("/")
def get_root():
    return RedirectResponse(url='/friends')
# O, 유저가 이상하면 로그인 페이지로, 유저가 일치하면 friend list화면으로
@app.get("/friends")
def get_friends(user=Depends(manager), db: Session = Depends(get_db)):
    if db.query(User).filter(User.name == user.name).first() is None:
        response = RedirectResponse("/login", status_code = 302)
        response.delete_cookie(key = "access-token")
        return response
    return FileResponse("friends.html")

@app.get("/login")
def get_login():
    return FileResponse("login.html")

#추가 구현 로그아웃페이지
@app.get("/register")
def get_register():
    return FileResponse("register.html")

# 채팅방 목록으로 이동
@app.get("/chatlist")
def get_chatlist():
    return FileResponse("chatlist.html")
# O
@app.get("/logout")
def logout(response: Response):
    response = RedirectResponse("/login", status_code = 302)
    response.delete_cookie(key = "access-token")
    return response
# O
@app.post("/register")
def register(user: UserSchema, db: Session = Depends(get_db)):
    return db_add_user(db, user)

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/current_user")
def get_current_user(user=Depends(manager)):
    return user.name
# O
@app.get("/getfriends")
def get_friends(user: str, db: Session = Depends(get_db)):
    return db_get_friends(db, user)
# O
@app.post("/addfriend")
def add_friend(friend:FriendSchema, db: Session = Depends(get_db)):
    return db_add_friend(db, friend.user1, friend.user2)

@app.get("/chatting/{friend}")
def chat_start(friend: str, db: Session = Depends(get_db)):
    return FileResponse("chatting.html")

@app.get("/getroom")
def get_room(user1:str, user2:str, db: Session = Depends(get_db)):
    return db_get_room(db, user1, user2)

# O
class ConnectionManager:
    def __init__(self):
        self.active_connections=[]

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

# O,웹소캣 기능
wsManager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await wsManager.connect(websocket)
    try:
        while True:
            data =await websocket.receive_text()
            await wsManager.broadcast(f"{data}")
    except Exception as e:
        pass
    finally:
        await wsManager.disconnect(websocket)

@app.post("/makeroom")
async def make_room(header: HeaderSchema, db: Session = Depends(get_db)):
    db_item = Header(from_id=header.from_id,
                    to_id=header.to_id,
                    last_chat=header.last_chat)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    print(db_item.id)
    return db_item.id
# O
@app.post("/updatelastchat")
def update_room(header: LastchatSchema, db: Session = Depends(get_db)):
    db_item = db.query(Header).filter(Header.id == header.header_id).first()
    db_item.last_chat = header.last_chat
    db.commit()
    db.refresh(db_item)
    return True

@app.get("/chat")
def get_chat(header_id: int,db: Session = Depends(get_db)):
    return db_get_chatlist(db, header_id)

@app.post("/chat")
async def add_chat(chat: ChatSchema, db: Session = Depends(get_db)):
    return db_add_chat(db, chat)

@app.get("/chatlists")
def get_chatlists(user: str, db: Session = Depends(get_db)):
    return db.query(Header).filter(or_(Header.from_id == user, Header.to_id == user)).all()

# O
def run():
    import uvicorn
    uvicorn.run(app, host='0.0.0.0')

if __name__ == "__main__":
    run()
