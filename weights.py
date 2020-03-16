

class Weights:

    def __init__(self):
        self.table = self.init_table()
        


    def init_table(self):
        d = {}
        with open("weights") as f:
            for line in f:
                ( k , v ) = line.split()
                d[ int(key) ] = v
        return d