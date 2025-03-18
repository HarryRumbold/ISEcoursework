from Baseline import random_search
from Tool import search
import os

# Pick a dataset

# Run baseline


# Run new tool
os.makedirs("new_search", exist_ok=True)
search("./datasets/Apache.csv",100,"new_search")

# compare results