from pymongo import MongoClient


class MongoDBHandle(object):
    """mongodb operate"""

    def __init__(self):
        """
        建立数据库连接
        """
        self.config = dict(host="127.0.0.1",
                           port=27017,
                           db_name="version1",
                           db_collection="mydb",
                           username="admin",
                           password="123456")
        self.client = MongoClient(self.config["host"], self.config["port"], username=f"{self.config['username']}",
                                  password=f"{self.config['password']}")
        self.db = self.client[f"{self.config['db_name']}"]
        self.collection = self.db[f"{self.config['db_name']}"]

    def close(self):
        self.client.close()

    def insert_code_one(self, content):
        mydict = {
            "input": content["input"],
            "output": content["output"],
            # "url": content["url"],
            # "time": content["time"]
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
    mongodb_connection = MongoDBHandle()
    dblist = mongodb_connection.client.list_database_names()
    collection_list = mongodb_connection.collection.find()
    print(dblist)
    print([x for x in collection_list])
    one = {"prompt": "Taobao", "code": "100", "url": "https://www.taobao.com", "time": ""}
    one_return = mongodb_connection.insert_code_one(one)
    print(one_return)
    mongodb_connection.close()
