import pandas as pd

data = pd.read_excel('fifo2.xlsx')


class Fifo:
    def __init__(self):
        self.data = {}
    def append(self, sym, data):
        if (self.data.get(sym)==None):
            self.data[sym] = []
        self.data[sym].append(data)
    def pop(self, sym):
        # FIFO
        if (self.data.get(sym)!=None):
            return self.data[sym].pop(0)
    def prepend(self, sym, data):
        # FIFO
        if (self.data.get(sym)!=None):
            self.data[sym].insert(0,data)
    def len(self, sym):
        if (self.data.get(sym)!=None):
            return len(self.data[sym])
        return 0
    def isEmpty(self, sym):
        if (self.data.get(sym)==None):
            return True
        if (len(self.data[sym]) > 0):
            return False
        else:
            return True


fifo = Fifo()


# Creating queue from the slice of by dataframe
for row in data[data['Type'] == 'buy'].itertuples():
    sym = row.Symbol
    item = {'units': row.Units, 'unit_value': row.Unit_Value}
    fifo.append(sym, item)



def calc_fifo(row):
    if (row['Type'] == 'sell'):
        sym = row['Symbol']
        unit_value = row['Unit_Value']
        units = row['Units']
        fifo_col = 0
        
        while True:
            # Exit loop if queue is empty or units are fully covered from queue
            if (units <= 0 or fifo.isEmpty(sym)):
                break
                
            # getting queue item
            f = fifo.pop(sym)
            
            if (units == f['units']):
                fifo_col = fifo_col + units * unit_value - f['units'] * f['unit_value']
                units = 0
                
            elif (units < f['units']):
                # adding back to queue what is left
                item = {'units': f['units'] - units, 'unit_value': f['unit_value']}
                fifo.prepend(sym, item)
                fifo_col = fifo_col + units * unit_value - units * f['unit_value']
                units = 0
                
            elif (units > f['units']):
                units = units - f['units']
                fifo_col =  fifo_col + f['units'] * unit_value - f['units'] * f['unit_value']
    
        row['fifo'] = fifo_col
        
    return row

result = data.apply(calc_fifo, axis=1)