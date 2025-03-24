import numpy as np
import pandas as pd
import math

budget = 23

distribution = np.array([0.4, 0.3, 0.2, 0.1])

print(distribution.sum())

distribution = np.repeat(distribution, budget/len(distribution))/int(budget/len(distribution))

distribution = np.pad(distribution, (0, budget%len(distribution)), 'constant')

print(len(distribution))

print(distribution.sum())

print(distribution)