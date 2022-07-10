#!/usr/bin/env python
# coding: utf-8

# In[27]:


import pandas as pd


# In[28]:


data = pd.read_excel('lifo.xlsx')


# In[29]:


data = data[ data['Symbol'] == 'BTC']


# In[30]:


class Fifo:
    def __init__(self):
        self.data = []
    def append(self, data):
        self.data.append(data)
    def pop(self):
        return self.data.pop()
    def prepend(self, data):
        # FIFO
        self.data.insert(0,data)
    def isEmpty(self):
        if (len(self.data) > 0):
            return False
        else:
            return True


# In[31]:


fifo = Fifo()


# In[32]:


fifo = Fifo()
def calc_fifo(row):
    if (row['Type'] == 'buy'):
        item = {'units': row['Units'], 'unit_value': row['Unit_Value']}
        fifo.append(item)
        
    if (row['Type'] == 'sell'):
        unit_value = row['Unit_Value']
        units = row['Units']
        fifo_col = 0
        
        while True:
            # Exit loop if queue is empty or units are fully covered from queue
            if (units <= 0 or fifo.isEmpty()):
                break
                
            # getting queue item
            f = fifo.pop()
            
            if (units == f['units']):
                fifo_col = fifo_col + units * unit_value - f['units'] * f['unit_value']
                units = 0
                
            elif (units < f['units']):
                # adding back to queue what is left
                item = {'units': f['units'] - units, 'unit_value': f['unit_value']}
                fifo.append(item)
                fifo_col = fifo_col + units * unit_value - units * f['unit_value']
                units = 0
                
            elif (units > f['units']):
                units = units - f['units']
                fifo_col =  fifo_col + f['units'] * unit_value - f['units'] * f['unit_value']
    
        row['fifo'] = fifo_col
        
    return row

data.apply(calc_fifo, axis=1)


# In[ ]:





# In[ ]:





# In[ ]:





# In[49]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[27]:





# In[ ]:




