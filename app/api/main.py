from fastapi import FastAPI
from base import dal
from sqlalchemy import select
app = FastAPI()

# if dal.connection == None:
#     dal.db_init()

@app.get("/")
def hello_world():
    return {"message": "OK"}


# @app.get('/tables')
# def list_tables():
#     tables = [dal.events.c.table_catalog, dal.events.c.table_schema, dal.events.c.table_name]
#     data = dal.connection.execute(select(tables)).fetchall()
#     return {"data": [x for x in data]}
