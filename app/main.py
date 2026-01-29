import os
from fastapi import FastAPI, Request, Depends, Form, WebSocket, WebSocketDisconnect, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

from .db import SessionLocal, engine, Base
from . import models, schemas, crud, auth


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Resume + Requests")


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await self.broadcast_count()

    def disconnect(self, websocket: WebSocket):
        try:
            self.active_connections.remove(websocket)
        except ValueError:
            pass

    async def broadcast_count(self):
        msg = {"online": len(self.active_connections)}
        for connection in list(self.active_connections):
            try:
                await connection.send_json(msg)
            except Exception:
               
                pass

manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    
    return templates.TemplateResponse("index.html", {"request": request, "email": "mahtab.nicknezhad@gmail.com", "skills": "Kotlin programmer"})

@app.get("/request", response_class=HTMLResponse)
def request_form(request: Request):
    return templates.TemplateResponse("request.html", {"request": request})

@app.get("/admin/login", response_class=HTMLResponse)
def admin_login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@app.get("/admin/requests", response_class=HTMLResponse)
def admin_requests_page(request: Request):
    return templates.TemplateResponse("admin_requests.html", {"request": request})


@app.post("/api/requests", response_model=schemas.ProjectRequestOut)
def create_project_request(item: schemas.ProjectRequestCreate, db: Session = Depends(get_db)):
    db_item = crud.create_request(db, item)
    return db_item

@app.post("/api/admin/login", response_model=schemas.Token)
def admin_login(username: str = Form(...), password: str = Form(...)):
    
    if username != auth.ADMIN_USERNAME or password != auth.ADMIN_PASSWORD:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = auth.create_access_token(data={"sub": username}, expires_delta=timedelta(hours=24))
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/admin/requests", response_model=List[schemas.ProjectRequestOut])
def list_requests(db: Session = Depends(get_db), current_admin: str = Depends(auth.get_current_admin)):
    return crud.get_all_requests(db)

@app.patch("/api/admin/requests/{request_id}", response_model=schemas.ProjectRequestOut)
def update_request(
    request_id: int,
    payload: schemas.ProjectRequestUpdate,
    db: Session = Depends(get_db),
    current_admin: str = Depends(auth.get_current_admin),
):
    db_item = crud.update_request(db, request_id, payload)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    return db_item

@app.delete("/api/admin/requests/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_admin: str = Depends(auth.get_current_admin),
):
    ok = crud.delete_request(db, request_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    return


@app.websocket("/ws/online")
async def websocket_online(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            
            data = await websocket.receive_text()
            
            await manager.broadcast_count()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast_count()
    except Exception:
        manager.disconnect(websocket)
        await manager.broadcast_count()


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 80))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")