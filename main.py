from fastapi import FastAPI, Depends, Response, Request
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

from models import Base, User
from schema import UserSchema
from database import SessionLocal ,engine
from crud import db_add_user

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

def run():
    import uvicorn
    uvicorn.run(app)

if __name__ == "__main__":
    run()