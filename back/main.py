from fastapi import FastAPI
from schemas import ProjectRequest
from fastapi import WebSocket

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Server is running"}


#ثبت درخواست

requests_list = []

@app.post("/request")
def create_request(data: ProjectRequest):
    requests_list.append(data)
    return {"status": "saved"}


@app.post("/login")
def login(username: str, password: str):
    if username == "admin" and password == "1234":
        return {"token": "fake-jwt-token"}
    return {"error": "unauthorized"}

@app.get("/admin/requests")
def get_requests(token: str):
    if token != "fake-jwt-token":
        return {"error": "forbidden"}
    return requests_list





#تعداد کاربر انلاین
online_users = 0

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    global online_users
    await ws.accept()
    online_users += 1
    await ws.send_text(str(online_users))
    try:
        while True:
            await ws.receive_text()
    except:
        online_users -= 1
