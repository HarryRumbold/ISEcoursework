from Baseline import random_search
from Tool import search
import os
from colorama import Fore, Back, Style

# Setup

datasets_folder = "datasets"
baseline_output_folder = "baseline_search"
tool_output_folder = "tool_search"

os.makedirs(baseline_output_folder, exist_ok=True)
os.makedirs(tool_output_folder, exist_ok=True)

budget = 100

# Run baseline

baseline_results = {}
for file_name in os.listdir(datasets_folder):
    if file_name.endswith(".csv"):
        file_path = os.path.join(datasets_folder, file_name)
        output_file = os.path.join(baseline_output_folder, f"{file_name.split('.')[0]}_search_results.csv")
        best_solution, best_performance = random_search(file_path, budget, output_file)

        baseline_results[file_name] = {
            "Best Solution": best_solution,
            "Best Performance": best_performance
        }

# Run new tool

tool_results = {}
for file_name in os.listdir(datasets_folder):
    if file_name.endswith(".csv"):
        file_path = os.path.join(datasets_folder, file_name)
        output_file = os.path.join(tool_output_folder, f"{file_name.split('.')[0]}_search_results.csv")
        best_solution, best_performance = search(file_path, budget, output_file)

        tool_results[file_name] = {
            "Best Solution": best_solution,
            "Best Performance": best_performance
        }

# Compare results

for file_name in os.listdir(datasets_folder):
    if(tool_results[file_name]['Best Performance'] <= baseline_results[file_name]['Best Performance']):
        print(Fore.GREEN + f"System: {file_name}")
    else:
        print(Fore.RED +   f"System: {file_name}")
    print(Fore.RESET +     f"    Baseline: {baseline_results[file_name]['Best Performance']}")
    print(                 f"    Tool:     {tool_results[file_name]['Best Performance']}")