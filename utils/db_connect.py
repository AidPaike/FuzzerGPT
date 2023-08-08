from pymongo import MongoClient


class MongoDBConn:

    def __init__(self, host, port, db_name, db_collection, username, password):
        """
        建立数据库连接
        """
        # self.client = MongoClient(f"mongodb://{host}:{port}/")
        self.client = MongoClient(host, port, username=f"{username}", password=f"{password}")
        self.db = self.client[f"{db_name}"]
        self.collection = self.db[f"{db_collection}"]

    def insert_code_one(self, content):
        mydict = {
            "prompt": content["prompt"],
            "code": content["code"],
            "url": content["url"],
            "time": content["time"]
        }

        ok = self.collection.insert_one(mydict)
        return ok

    def inser_code_many(self, contents):
        mylist = [
            {"prompt": "Taobao", "code": "100", "url": "https://www.taobao.com", "time": ""},
            {"prompt": "Taobao", "code": "100", "url": "https://www.taobao.com", "time": ""},
            {"prompt": "Taobao", "code": "100", "url": "https://www.taobao.com", "time": ""}
        ]
        ok = self.collection.insert_many(contents)
        return ok


if __name__ == '__main__':
    mongodb_connection = MongoDBConn(host="127.0.0.1",
                                     port=27017,
                                     db_name="test",
                                     db_collection="mydb",
                                     username="aidpaike",
                                     password="123456")
    dblist = mongodb_connection.client.list_database_names()
    collection_list = mongodb_connection.collection.find()
    print(dblist)
    print([x for x in collection_list])
