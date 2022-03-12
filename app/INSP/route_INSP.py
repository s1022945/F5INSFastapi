import json
import datetime
import pandas as pd
from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.INSP.EQDailyCheck.config import DAILY_ITEM_DICT
from app.INSP.database import dbSetting_EQDAILY
import app.INSP.EQDailyCheck.EQDailyCheck as EQDailyCheck
# import app.dashboard.SPME as SPME
# import app.dashboard.crud as crud

router = APIRouter(
    prefix="/INSP",
    tags=["INSP"],
)

templates = Jinja2Templates(directory="templates")

# Dependency
def db_EQDAILY():
    db = dbSetting_EQDAILY.session()
    try:
        yield db
    finally:
        db.close()
# def db_F5FABIT():
#     db = dbSetting_F5FABIT.session()
#     try:
#         yield db
#     finally:
#         db.close()
# def db_SPME_SPECIAL_CASE():
#     db = dbSetting_SPME_SPECIAL_CASE.session()
#     try:
#         yield db
#     finally:
#         db.close()
@router.get("/EQDailyCheck")
def EQDailyCheck_SUM(request: Request):
    return templates.TemplateResponse("EQDailyCheck_SUM.html",\
        {
            "request": request,
            "DAILY_ITEM_DICT" : DAILY_ITEM_DICT
        }
        )

@router.get("/EQDailyCheck/GET_STATUS")
def EQDailyCheck_GET_STATUS(request: Request, db_EQDAILY: Session = Depends(db_EQDAILY)):
    itemList = []
    for AREA in DAILY_ITEM_DICT:
        for LINE in DAILY_ITEM_DICT[AREA]:
            for EQ in DAILY_ITEM_DICT[AREA][LINE]:
                for ITEM in DAILY_ITEM_DICT[AREA][LINE][EQ]:
                    itemList.append(EQ + "_" + ITEM)
    dt = ""
    now = datetime.datetime.now()
    totalSeconds = (now - datetime.datetime(now.year, now.month, now.day, 6, 30, 0)).total_seconds()

    if totalSeconds <= 0:
        tmpDt = now + datetime.timedelta(days = -1)
        dt = datetime.datetime(tmpDt.year, tmpDt.month, tmpDt.day, 18, 30, 0)
    elif totalSeconds <= 43200:
        dt = datetime.datetime(now.year, now.month, now.day, 6, 30, 0)
    else:
        dt = datetime.datetime(now.year, now.month, now.day, 18, 30, 0)
    
    # dt = datetime.datetime(now.year, now.month, now.day, 16, 30, 0)

    sqlstr = r'SELECT * FROM `STAT_SUM`' 
    df = pd.read_sql_query(text(sqlstr), db_EQDAILY.bind)
    df["ITEM"] = df["EQPT_ID"] + "_" + df["DATA_GROUP"]
    df.loc[(df["MEAS_DTTM"] < dt) & (df["STATUS"] == "OK"), "STATUS"] = "OVERTIME"
    df["MEAS_DTTM"] = df["MEAS_DTTM"].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
    df["SYS_UPDATE_STAMP"] = df["SYS_UPDATE_STAMP"].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
    df = df[df["ITEM"].isin(itemList)]
    print(type(df[df["STATUS"] == "OK"].count()["ITEM"]))
    res = {
        "summary":{
            "total": len(itemList), 
            "OK": int(df[df["STATUS"] == "OK"].count()["ITEM"]), 
            "OOS": int(df[df["STATUS"] == "OOS"].count()["ITEM"]), 
            "OOC": int(df[df["STATUS"] == "OOC"].count()["ITEM"]), 
            "OVERTIME": int(df[df["STATUS"] == "OVERTIME"].count()["ITEM"])
            },
            "updateTime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "itemList": itemList,
            "data": df.T.to_dict()
        }
    return res

@router.api_route("/EQDailyCheck/UPDATE_RAW_DATA", methods=["GET", "POST"])
async def EQDailyCheck_UPDATE_RAW_DATA(request: Request, db_EQDAILY: Session = Depends(db_EQDAILY)):
    req_info = ""
    try:
        req_info = await request.json()
        # print(req_info)
        if req_info["EQ"][:4] == "ILSP":
            # print("req_info = ", req_info)
            EQDailyCheck.ILSPData2DB(req_info, db_EQDAILY)
            return "OK"

        elif req_info["EQ"][:4] == "SPME":
            # print("req_info = ", req_info)
            EQDailyCheck.SPMEData2DB(req_info, db_EQDAILY)
            return "OK"
        
        elif req_info["EQ"][:4] == "SUFP":
            # print("req_info = ", req_info)
            EQDailyCheck.SUFPData2DB(req_info, db_EQDAILY)
            return "OK"
    except Exception as e:
        print(repr(e))
        print("Parse data failed...")
        return "Parse data failed..."
    # finally:
    #     return "OK"