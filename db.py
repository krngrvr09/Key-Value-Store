import psutil
from memory_profiler import profile

class DB:
    _instance = None

    def __new__(cls, filepath):
        if cls._instance is None:
            cls._instance = super(DB, cls).__new__(cls)
        cls._instance.filepath = filepath
        cls._instance.mp = {}
        cls._instance.load(filepath)
        return cls._instance
    
    # def __init__(self, filepath):
    #     self.filepath = filepath
    #     self.mp = {}
    #     self.load(filepath)
    
    # @profile
    def load(self, filepath):
        with open(filepath, 'r') as file:
            for line in file:
                tokens = line.split()
                self.mp[tokens[0]] = " ".join(tokens[1:])
    # @profile
    def get(self,key):
        if key in self.mp:
            return {"status": 200, "data": self.mp[key]}
        else:
            return {"status": 404}

    # @profile
    def slow_get(self,key):
        with open(self.filepath, 'r') as file:
            for line in file:
                tokens = line.split()
                if tokens[0]==key:
                    return {"status": 200, "data": " ".join(tokens[1:])}
            
        return {"status": 404}

db = DB("example.data")
print(db.slow_get("b8504438-d09e-439c-bd71-d55e28538ecb"))