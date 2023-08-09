
class TNode:
    def __init__(self, c, is_end=False):
        self.c = c
        self.end = is_end
        self.val = ""
        self.mp = {}

    def _add(self, key, idx, val):
        if idx==len(key):
            self.end = True
            self.val = val
            return
        if key[idx] not in self.mp:
            self.mp[key[idx]] = TNode(key[idx])
        self.mp[key[idx]]._add(key,idx+1,val)

    def add(self, key, val):
        self._add(key,0,val)
    
    def _get( self, key, idx):
        if idx==len(key):
            if self.end:
                return self.val
            else:
                return None
        if key[idx] not in self.mp:
            return None
        return self.mp[key[idx]]._get(key,idx+1)

    def get(self, key):
        return self._get(key,0)

class DB:

    def __init__(self, filepath):
        self.filepath = filepath
        # self.mp = {}
        self.root = TNode("#")
        self.load(filepath)
    
    def load(self, filepath):
        with open(filepath, 'r') as file:
            for line in file:
                tokens = line.split()
                self.root.add(tokens[0], " ".join(tokens[1:]))
                # self.mp[tokens[0]] = " ".join(tokens[1:])
    
    def get(self,key):
        res = self.root.get(key)
        if res is None:
            return {"status": 404}
        
        return {"status": 200, "data": res}
        # if key in self.mp:
        #     return {"status": 200, "data": self.mp[key]}
        # else:
        #     return {"status": 404}

    def slow_get(self,key):
        with open(self.filepath, 'r') as file:
            for line in file:
                tokens = line.split()
                if tokens[0]==key:
                    return {"status": 200, "data": " ".join(tokens[1:])}
            
        return {"status": 404}
