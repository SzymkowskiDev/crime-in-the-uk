import pymongo


class DataAccessLayer:
    # add os.env
    host = None
    username = None
    password = None
    connection = None

    def __init__(self, host):        
        self.host = host,

    def mongo_init(self):
        self.connection = pymongo.MongoClient(
            host = self.host,
        )
          
        
    
# dal = pymongo.MongoClient(host ='127.0.0.1:27018', username = 'root' ,password = 'abc123' )
dal = DataAccessLayer("mongodb://root:abc123@mongo_raw") #for container
# dal = DataAccessLayer("mongodb://root:abc123@mongo_raw") #for local tbc




