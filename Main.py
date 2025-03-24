from Baseline import random_search
from Tool import search
import os
from colorama import Fore, Back, Style
import pandas as pd

# Setup

datasets_folder = "datasets"
baseline_output_folder = "baseline_search"
tool_output_folder = "tool_search"

os.makedirs(baseline_output_folder, exist_ok=True)
os.makedirs(tool_output_folder, exist_ok=True)

budget = 100

# Loop the test

baseline = 0
tool = 0

file_results = {
    "7z.csv": 0,
    "Apache.csv": 0,
    "brotli.csv": 0,
    "LLVM.csv": 0,
    "PostgreSQL.csv": 0,
    "spear.csv": 0,
    "storm.csv": 0,
    "x264.csv": 0
}

no_of_tests = 1

for i in range(no_of_tests):

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
            tool = tool + 1
            file_results[file_name] = file_results[file_name] + 1
        else:
            print(Fore.RED +   f"System: {file_name}")
            baseline = baseline + 1
        print(Fore.RESET +     f"    Baseline: {baseline_results[file_name]['Best Performance']}")
        print(                 f"    Tool:     {tool_results[file_name]['Best Performance']}")

    # Sum performance in result files

    #for file_name in os.listdir(baseline_output_folder):
    #    if file_name.endswith(".csv"):
    #        csv = pd.read_csv(os.path.join(baseline_output_folder, file_name))
    #        csv2 = pd.read_csv(os.path.join(tool_output_folder, file_name))
    #        print("Performance sum of ",file_name)
    #        print(csv.iloc[:,-1:].sum().iloc[0])
    #        print(csv2.iloc[:,-1:].sum().iloc[0])


print(f"Scores over {no_of_tests} runs")
print("Baseline: ", baseline)
print("Tool: ", tool)

for file in file_results:
    print(file, " ", file_results[file])