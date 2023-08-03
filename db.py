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
    
    def load(self, filepath):
        with open(filepath, 'r') as file:
            for line in file:
                tokens = line.split()
                self.mp[tokens[0]] = " ".join(tokens[1:])
    
    def get(self,key):
        if key in self.mp:
            return {"status": 200, "data": self.mp[key]}
        else:
            return {"status": 404}
