from Baseline import random_search
from Tool import search
import os
from colorama import Fore, Back, Style
import pandas as pd
import math

#########
# Setup #
#########

datasets_folder = "datasets"
baseline_output_folder = "baseline_search"
tool_output_folder = "tool_search"

os.makedirs(baseline_output_folder, exist_ok=True)
os.makedirs(tool_output_folder, exist_ok=True)

##############
# User input #
##############

# Set budget
budget = 100

try:
    userInput = int(input(f"Enter budget (default={budget}): "))
except ValueError:
    userInput = -1

if(userInput >= 0):
    budget = userInput

print(f"Budget set to {budget}")

# Test one or all datasets?
userInput = ''
while (userInput != 'y' and userInput != 'n'):
    userInput = input("Test all datasets? (y/n): ").lower()

# Test one dataset
if(userInput == 'n'):
    # Iterate over a list of files in directory
    filelist = [files for files in os.listdir(datasets_folder)]

    # Convert the files list to a dictionary
    filelist_dict = { ind: name for (ind,name) in enumerate(filelist) }

    # Display files in the dataset file
    for idx, file in filelist_dict.items():
        print(f"[{idx}] {file}")

    try:
        userInput = int(input("Enter a number: "))
    except ValueError:
        userInput = -1
    
    # If a valid file is selected
    if(userInput >= 0 and userInput < len(filelist_dict)):
        file_name = filelist_dict[userInput]
        print(f"Selected {file_name}")

        no_of_tests = 1
        try:
            userInput = int(input(f"Enter number of tests (default={no_of_tests}): "))
        except ValueError:
            userInput = -1

        if(userInput >= 0):
            no_of_tests = userInput
        
        print(f"Number of tests set to {no_of_tests}")

        tool_score = 0
        baseline_worst_performance, tool_worst_performance = 0, 0
        baseline_highest_performance, tool_highest_performance = math.inf, math.inf
        for i in range(no_of_tests):
            file_path = os.path.join(datasets_folder, file_name)
            # Test baseline
            output_file = os.path.join(baseline_output_folder, f"{file_name.split('.')[0]}_search_results.csv")
            baseline_best_solution, baseline_best_performance = random_search(file_path, budget, output_file)
            if baseline_best_performance < baseline_highest_performance:
                baseline_highest_performance = baseline_best_performance
            if baseline_best_performance > baseline_worst_performance:
                baseline_worst_performance = baseline_best_performance
            # Test tool
            output_file = os.path.join(tool_output_folder, f"{file_name.split('.')[0]}_search_results.csv")
            tool_best_solution, tool_best_performance = search(file_path, budget, output_file)
            if tool_best_performance < tool_highest_performance:
                tool_highest_performance = tool_best_performance
            if tool_best_performance > tool_worst_performance:
                tool_worst_performance = tool_best_performance
            # Display results
            if(tool_best_performance <= baseline_best_performance):
                print(Fore.GREEN + f"Run {i+1}:")
                tool_score = tool_score + 1
            else:
                print(Fore.RED + f"Run {i+1}:")
            print(Fore.RESET + f"    Baseline: {baseline_best_performance} {baseline_best_solution}")
            print(Fore.RESET + f"    Tool:     {tool_best_performance} {tool_best_solution}")
        print(f"Tool results for {file_name}: {tool_score}/{no_of_tests}")
        print(f"Range of Baseline: ", baseline_worst_performance - baseline_highest_performance)
        print(f"Range of Tool: ", tool_worst_performance - tool_highest_performance)
    else:
        print(f"Invalid Entry \'{userInput}\'")

# Test all datasets
if(userInput == 'y'):

    no_of_tests = 1
    try:
        userInput = int(input(f"Enter number of tests (default={no_of_tests}): "))
    except ValueError:
        userInput = -1

    if(userInput >= 0):
        no_of_tests = userInput
    
    print(f"Number of tests set to {no_of_tests}")

    # Set scores for each tool
    baseline = 0
    tool = 0

    # Iterate over a list of files in directory
    filelist = [files for files in os.listdir(datasets_folder)]

    # Convert the files list to a dictionary, and set the scores to 0
    file_results = { name : 0 for name in filelist }

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
        print(Fore.YELLOW + '-' * 8, f"Run {i+1}", '-' * 8)
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


    print(Fore.YELLOW + f"-- Results over {str(no_of_tests).ljust(2)} runs --")
    print(Fore.RESET + f"Baseline  {baseline:>16}")
    print(f"Tool      {tool:>16}")
    print('-' * 26)
    for file in file_results:
        print(f"{file:<15} {file_results[file]:>10}")