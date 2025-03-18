import numpy as np
import pandas as pd
import math

# evenly spaced
x = [1, 4, 6, 8, 18, 20, 34]

#print(x[::int(np.ceil( len(x) / 20 ))])

#sampled_config = [int(np.random.choice(data[col].unique())) for col in config_columns]

#y = [int(np.random.uniform(data[col].unique().min(), data[col].unique().max(), budget)) for col in config_columns]

#print(np.random.uniform(min(x), max(x), 3))

budget = 14

#for i in range(0,len(x),math.ceil(len(x)/budget)):
    #print(x[math.floor(len(x)/budget*i)])
 #   print(x[i])

#print(np.random.choice([1,2,3],3,p=[0.1,0.2,0.7]))

#print(np.random.choice([1,2,3]))

x = [1,2,3]
y = [4,5,6]

z = []

#np.append(z,x,axis=1)
#np.append(z,y,axis=1)

#z = zip(x, y)
#z = zip(z, x)

i = 0

data = pd.DataFrame()
data[i] = x
i = 1
data[i] = y

print(data)