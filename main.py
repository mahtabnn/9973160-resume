from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from schemas import ProjectRequest

app = FastAPI()

# ذخیره موقت درخواست‌ها
requests_list = []

# شمارش کاربران آنلاین
online_users = 0


@app.get("/")
def home():
    return {"message": "Server is running"}


# ثبت درخواست پروژه
@app.post("/request")
def create_request(data: ProjectRequest):
    requests_list.append(data)
    return {"status": "saved"}


# دیدن همه درخواست‌ها (ادمین ساده)
@app.get("/admin/requests")
def get_requests():
    return requests_list


# WebSocket برای کاربران آنلاین
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    global online_users
    await ws.accept()
    online_users += 1
    await ws.send_text(str(online_users))

    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        online_users -= 1
