from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

class RequestData(BaseModel):
    name: str
    email: str
    project_type: str
    budget: str
    description: str


@app.get("/", response_class=HTMLResponse)
async def home():
    with open("index.html", encoding="utf-8") as f:
        return f.read()


@app.post("/request")
async def receive_request(data: RequestData):
    print(data)
    return {"status": "ok"}


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    await ws.send_text("کاربر آنلاین است")
    while True:
        await ws.receive_text()
