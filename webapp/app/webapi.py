from pymongo import MongoClient
import config as config



class webapi:
    def __init__(self, MongoConnectionString) -> None:
        self.conn = MongoClient(MongoConnectionString)
        self.base = self.conn["inventory"]
        self.inventory = self.base["inventory"]
        self.history = self.base["history"]

    def getHistory(self, field=None, value=None, sortField = "collect_date", sortArray = -1) -> list:
        if field == None:
            return [i for i in self.history.find({}, {"_id": False})]
        else:
            return [i for i in self.history.find({field: value}, {"_id": False}).sort(sortField, sortArray)] if field in ["username", "computername"] else []
        
    def getComputerInfo(self, computername):
        return [i for i in self.inventory.find({"computername": computername}, {"_id": False})]
        

    def test():
        return "Ok"