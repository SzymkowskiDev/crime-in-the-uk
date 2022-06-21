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
            # username = self.username,
            # password = self.password
        )
        
    
# dal = DataAccessLayer("mongodb://root:abc123@mongo_raw")
dal = DataAccessLayer("mongodb://root:abc123@mongo_raw")

