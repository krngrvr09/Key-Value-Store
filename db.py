
class DB:

    def __init__(self, filepath):
        self.filepath = filepath
        self.mp = {}
        self.load(filepath)
    
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

    def slow_get(self,key):
        with open(self.filepath, 'r') as file:
            for line in file:
                tokens = line.split()
                if tokens[0]==key:
                    return {"status": 200, "data": " ".join(tokens[1:])}
            
        return {"status": 404}
