from Baseline import random_search
from Tool import search
import os

# setup

datasets_folder = "datasets"
baseline_output_folder = "baseline_search"
tool_output_folder = "new_search"

os.makedirs(baseline_output_folder, exist_ok=True)
os.makedirs(tool_output_folder, exist_ok=True)

budget = 100

# Run baseline


# Run new tool

for file_name in os.listdir(datasets_folder):
    if file_name.endswith(".csv"):
        file_path = os.path.join(datasets_folder, file_name)
        output_file = os.path.join(tool_output_folder, f"{file_name.split('.')[0]}_search_results.csv")
        search(file_path, budget, output_file)

# compare results