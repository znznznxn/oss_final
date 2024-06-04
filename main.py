from fastapi import FastAPI, Depends, Response, Request, WebSocket
from fastapi.responses import FileResponse, RedirectResponse

from sqlalchemy import or_
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

from models import Base, User, Header
from schema import UserSchema, FriendSchema, HeaderSchema, ChatSchema
from database import SessionLocal ,engine
from crud import db_add_user, db_add_friend, db_get_friends, db_get_room, db_get_chatlist, db_add_chat

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class NotAuthneticatedException(Exception):
    pass

SECRET = "oss"

manager = LoginManager(SECRET, '/login', use_cookie=True, custom_exception=NotAuthneticatedException)

# 사용자 인증 및 access_token 부여
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

# 사용자 인증 확인
@app.exception_handler(NotAuthneticatedException)
def auth_exception_handler(request: Request, exc: NotAuthneticatedException):
    return RedirectResponse('/login')

@manager.user_loader
def get_user(username: str, db: Session = None):
    if not db:
        with SessionLocal() as db:
            return db.query(User).filter(User.name == username).first()
    return db.query(User).filter(User.name == username).first()

# 로그인 상태 시 친구 목록 창으로 redirect
@app.get("/")
def get_root():
    return RedirectResponse(url='/friends')

@app.get("/friends")
def get_friends(user=Depends(manager)):
    return FileResponse("friends.html")

@app.get("/login")
def get_login():
    return FileResponse("login.html")

# 채팅방 목록으로 이동
@app.get("/chatlist")
def get_chatlist():
    return FileResponse("chatlist.html")

@app.get("/logout")
def logout(response: Response):
    response = RedirectResponse("/login", status_code = 302)
    response.delete_cookie(key = "access-token")
    return response

@app.post("/register")
def register(user: UserSchema, db: Session = Depends(get_db)):
    return db_add_user(db, user)

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/current_user")
def get_current_user(user=Depends(manager)):
    return user.name

@app.get("/getfriends")
def get_friends(user: str, db: Session = Depends(get_db)):
    return db_get_friends(db, user)

@app.post("/addfriend")
def add_friend(friend:FriendSchema, db: Session = Depends(get_db)):
    return db_add_friend(db, friend.user1, friend.user2)

@app.get("/chatting/{friend}")
def chat_start(friend: str, db: Session = Depends(get_db)):
    return FileResponse("chatting.html")

@app.get("/getroom")
def get_room(user1:str, user2:str, db: Session = Depends(get_db)):
    return db_get_room(db, user1, user2)

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

@app.get("/chat")
def get_chat(header_id: int,db: Session = Depends(get_db)):
    return db_get_chatlist(db, header_id)

@app.post("/chat")
async def add_chat(chat: ChatSchema, db: Session = Depends(get_db)):
    return db_add_chat(db, chat)

@app.get("/chatlists")
def get_chatlists(user: str, db: Session = Depends(get_db)):
    return db.query(Header).filter(or_(Header.from_id == user, Header.to_id == user)).all()


def run():
    import uvicorn
    uvicorn.run(app)

if __name__ == "__main__":
    run()