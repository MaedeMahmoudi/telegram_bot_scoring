import couchdb
from datetime import datetime

class couchDatabase:

    def __init__(self , url ,db_name):
        couch = couchdb.Server(url)
        if db_name in couch:
            db = couch[db_name]
        else:
            db = couch.create(db_name)
        self.db = db
    def getUser(self, user_id):
        getuser = self.db.get("user:"+user_id)
        if getuser:
            return getuser
        else:
            return            
    def addPoints(self , user_id , points):
        getuser = self.db.get("user:"+user_id)
        if getuser:
            print("User exists")
            getuser["points"] += points
            self.db.save(getuser)
            print("Points added")

        else:
            user_doc = {
            "_id": f"user:{user_id}",
            "type": "user",
            "telegram_id": user_id,
            "points": points,
            "last_active": datetime.now().isoformat()}
            self.db.save(user_doc)
            print("User does not exist")

couchdb = couchDatabase("http://admin:password@host:port/" , "users")
couchdb.addPoints("12345634" , 100)
