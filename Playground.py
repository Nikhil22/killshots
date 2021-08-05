#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


df = pd.DataFrame({
    'a':["cat","cat","mouse","mouse","dog", "dog"],
    'b':["time1","time2","time1","time2","time1","time2"],
    'c':[10,11,12,13,14,15]
})
df.set_index(['a','b'], inplace=True)

print ("-------------------Basic data frame-------------------")
display(df)
    
print ("-------------------Iterating-------------------")
for time, row in df.loc["cat"].itertuples():
    print(time, row)
    
def m(row):
    return str(row.c) + " " + str(row.name)
  
print ("-------------------Applying-------------------")
aa = df.loc["cat"].apply(m, axis=1)
display(aa)


# In[3]:


print ("------------------Group by-------------------")

idxTosubDF = {}

for a, subDF in df.groupby(level=0):
    print ("\n---Index---\n")
    print ((a))
    print ("\n---subDF---\n")
    print (subDF)
    print ("\n---locking on subDF---\n")
    print (subDF.loc[a])
    print ("\n---locking on subDF, on last element of c---\n")
    print (subDF.loc[a].c.iloc[-1])
    print ("\n---locking on subDF, index of last element of c---\n")
    print (subDF.loc[a].index[-1])
    idxTosubDF[a] = subDF
    
print ("------------------idxTosubDF dictionary-------------------")
print (idxTosubDF)


# In[4]:


print ("------------------Access list of c for an index-------------------")

print (idxTosubDF["cat"]["c"].tolist())


# In[5]:


prices = [1,2,3,4,5]

for i in range(len(prices)):
    index = len(prices) - i - 1
    print ("leading index", index)
    print ("leading price", prices[index])


# In[27]:


def bottom(prices):
    '''
    leading bottom must be >= to lowest point and to its right
    current price must be > leading bottom price
    '''
    leadingBottom = None
    lowestPoint = {"value": prices[0], "index": 0}
    currentPrice = prices[-1]
        
    for i in range(len(prices)):
        index = len(prices) - i - 1
        price = prices[index]
        if price < lowestPoint['value']:
            lowestPoint = {"value": price, "index": index}
                
        if index < len(prices) - 1 and index > 0:
            mid = price
            right = prices[index + 1]
            left = prices[index -1]
            if isEmpireBottom(mid, left, right):
                if leadingBottom is None:
                    leadingBottom = {"value": price, "index": index}
            
    state = (
        leadingBottom is not None
        and leadingBottom['value'] >= lowestPoint['value']
        and leadingBottom['index'] > lowestPoint["index"]
        and currentPrice > leadingBottom['value']
    )
        
    return {
        "state": state,
        "lowestPrice": lowestPoint['value'],
        "leadingBottomPrice": leadingBottom['value'] if leadingBottom is not None else None,
        "currentPrice": currentPrice
    }
        
    
def isEmpireTop(mid, left, right):
    return mid > right and mid > left

def isEmpireBottom(mid, left, right):
    return mid < right and mid < left
    

assert bottom([7,5,8,6,7])["state"] is True
assert bottom([7,5,8,6])["state"] is False
assert bottom([7,5,8,6,5])["state"] is False
assert bottom([7,1,8,6,5,2,3])["state"] is True
assert bottom([7,8,1,3,2,4,0.5, 4, -1])["state"] is False
assert bottom([7,8,1,3,2,4, 1.2, 4, 1])["state"] is False
assert bottom([7,8,1,3,2,4, 1.2, 4, 1.3])["state"] is True
assert bottom([7,8,1,3,2,4, 1.2, 4, 1])["state"] is False
assert bottom([5,4,3,2,1])["state"] is False
assert bottom([1,2,3,4,5])["state"] is False


# In[7]:


series = df.loc["cat"]["c"]
display(series)
print ("------------------Slicing a series, last N elements-------------------")
display(series[-1:])


# In[ ]:





# In[ ]:


