from fastapi import FastAPI
from sqlalchemy import select
try: from base import dal
except: from .base import dal

app = FastAPI()

if dal.connection == None:
    dal.db_init()

@app.get("/")
def hello_world():
    return {"message": "OK"}


# @app.get('/tables')
# def list_tables():
#     tables = [dal.events.c.table_catalog, dal.events.c.table_schema, dal.events.c.table_name]
#     data = dal.connection.execute(select(tables)).fetchall()
#     return {"data": [x for x in data]}
