try: from .base import PostgresDal
except: pass
try: from base import PostgresDal
except: pass
from datetime import datetime
from sqlalchemy import select
try: from .base import MongoDal
except: pass
try: from base import MongoDal
except: pass




class MongoForArticles:     
    

    def __init__(self, client):
        self.client = client


    def extract_data(self):
        # there is possibility to rewrite it as
        # this method may hit limit due to multiple rows

        db = self.client["web_content"]
        col = db["articles"]
        data = [x for x in col.find({},{})]
        return data

class PostgresForArticles:     
    

    def __init__(self, client):
        self.client = client


    def add_event(self, mongo_id:str, title:str, post_date:datetime, link:str, content:str):
        ins = self.client.articles.insert()

        self.client.connection.execute(ins,
            mongo_id = mongo_id,
            title = title,
            post_date = post_date,
            link = link,
            content = content
        )



if __name__ == '__main__':
    if MongoDal.connection == None:
        MongoDal.mongo_init()
    
    if PostgresDal.connection == None:
        PostgresDal.db_init()

    mongo_client = MongoDal.connection
    postgres_client = PostgresDal
