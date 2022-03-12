import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.INSP import route_INSP

# from app.dashboard.database import dbSetting_cf5insp_1e1r
# import app.dashboard.crud as crud
# import cf5_fastapi.models as models


# models.Base.metadata.create_all(bind=engine)
# models.Base.metadata.create_all(bind = dbSetting_cf5insp_1e1r.engine)
import os
# os.system("title cf5_fastapi")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(
    route_INSP.router,
    # prefix="/INSP"
    )

# app.include_router(
#     route_SPME.router,
#     prefix="/DASHBOARD")

# app.include_router(
#     route_AICM.router,
#     prefix="/DASHBOARD")
# app.include_router(
#     route_report_RVRP.router,
#     prefix='/REPORT'
# )
# Dependency
# def db_cf5insp_1e1r():
#     db = dbSetting_cf5insp_1e1r.session()
#     try:
#         yield db
#     finally:
#         db.close()

@app.get("/")
async def index(request: Request):
    # body = b''
    # async for chunk in request.stream():
    #     body += chunk
    # RecipeRecord = body.decode("UTF-8")
    return templates.TemplateResponse("index.html", {"request": request})