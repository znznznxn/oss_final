from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/login")
def get_login():
    return FileResponse("login.html")

def run():
    import uvicorn
    uvicorn.run(app)

if __name__ == "__main__":
    run()