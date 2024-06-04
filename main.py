from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from models import Base
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

@app.get("/login")
def get_login():
    return FileResponse("login.html")

@app.post("/register")
def register(user: UserSchema, db: Session = Depends(get_db)):
    return db_add_user(db, user)

def run():
    import uvicorn
    uvicorn.run(app)

if __name__ == "__main__":
    run()