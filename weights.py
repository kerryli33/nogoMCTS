

class Weights:

    def __init__(self):
        self.table = self.init_table()
        


    def init_table(self):
        d = {}
        with open("weights") as f:
            for line in f:
                ( k , v ) = line.split()
                d[ int(k) ] = float(v)
        return d
    
    def get(self, code):
        return self.table.get(code, -1)