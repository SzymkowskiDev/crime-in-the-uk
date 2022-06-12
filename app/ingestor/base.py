import pymongo


class DataAccessLayer:
    # add os.env
    host = None
    username = None
    password = None
    connection = None

    def __init__(self, host, username, password):
        self.host = host,
        self.username = username
        self.password = password

    def mongo_init(self):
        self.connection = pymongo.MongoClient(
            host = self.host,
            username = self.username,
            password = self.password
        )
        
    
dal = DataAccessLayer("mongodb://localhost:27018", "root", "abc123")


