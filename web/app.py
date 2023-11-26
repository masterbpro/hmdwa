import datetime
import os
import sys

import pytz
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
import uvicorn
import pymongo
import certifi
from models import Alarm


uri = os.getenv("DB_URI")
if not uri:
    sys.exit("DB_URI is not set! Exiting...")

app = FastAPI()
templates = Jinja2Templates(directory="templates")
timezone = pytz.timezone("Europe/Moscow")


@app.on_event("startup")
def start():
    app.mongodb_client = pymongo.MongoClient(uri, tlsCAFile=certifi.where())
    app.db = app.mongodb_client["hmdwa"]
    app.status = app.db.status


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    query = app.db.alarm.find_one()
    result = Alarm(**query)
    days_without_alarm = datetime.datetime.now(timezone) - result.alarm_at

    return templates.TemplateResponse(
        "index.html",
        context={
            "request": request,
            "days_without_alarm": days_without_alarm.days,
            "last_update": result.alarm_at.strftime("%H:%M %d.%m.%Y"),
        },
    )


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
