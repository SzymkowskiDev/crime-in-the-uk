import time
import datetime
try: from base import dal
except: from .base import dal

def scrapper():
    pass

def checkForArticle(myClient,content):
    appdb = myClient["web_content"]
    appcoll = appdb["articles"]
    # appcoll.find({},{ "_id": 0, "name": 1, "address": 1 })
    if appcoll.find({},{ "location":content[0]}):
        return False
    else:
        return True

def insertArticle(myClient, dateTime):
    data = {
        "dateTime":dateTime,
        "eventName": "Test",
        "content": [1,2,3,4,5],
        "location":"NY"
    }
    appdb = myClient["web_content"]
    appcoll = appdb["articles"]
    appcoll.insert_one(data)






def proc(myClient):
        # content = scrapper check on scrape level if article exist in db
        # if checkForArticle(myClient, content = ("NY")) == True:
            insertArticle(myClient, dateTime = datetime.datetime.now())

if __name__ == '__main__':
    if dal.connection == None:
        dal.mongo_init()

    myClient = dal.connection

    while True:
        time.sleep(10)
        
        proc(myClient)

