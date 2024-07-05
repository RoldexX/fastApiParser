from fastapi import FastAPI
from fastapi.responses import JSONResponse
from json import loads
from parser import start_parse

from read_csv import get_news_json


app = FastAPI()


@app.get("/")
async def root():

    return JSONResponse(loads(get_news_json()))


@app.get("/start_parse/")
async def start_parse_process():
    start_parse()
    return {"message": f"Данные успешно спашены"}
