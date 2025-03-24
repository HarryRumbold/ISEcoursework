import pandas as pd
import numpy as np
import os
import random
import matplotlib.pyplot as plt
import math

# Suppress pandas deprecation warnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Remove scientific notation e.g. 3.487e+03, easier for testing
np.set_printoptions(suppress=True)

def search(file_path, budget, output_file):

    # Hyperparameters
    # Percentage used in step 1
    SAMPLE_BUDGET = 0.5 * budget

    # Remaining budget to be used in step 2
    REMAINING_BUDGET = budget - SAMPLE_BUDGET

    # Load the dataset
    data = pd.read_csv(file_path)

    # Identify the columns for configurations and performance
    config_columns = data.columns[:-1]
    performance_column = data.columns[-1]

    # Maximisation or Minimisation?
    system_name = os.path.basename(file_path).split('.')[0]
    if system_name.lower() == "---":
        maximization = True
    else:
        maximization = False

    # Extract the best and worst performance values
    if maximization:
        worst_value = data[performance_column].min() / 2  # For missing configurations
    else:
        worst_value = data[performance_column].max() * 2  # For minssing configrations
    
    # Initialize the best solution and performance
    best_performance = -np.inf if maximization else np.inf
    best_solution = []

    ###################
    # Actually search #
    ###################

    # Create first samples, sampled_config is a batch of configurations
    sampled_config = pd.DataFrame()
    for col in config_columns:
        # start with a uniformly random spread using 50% of the budget
        column_config = np.random.choice(data[col].unique(), int(SAMPLE_BUDGET))
        random.shuffle(column_config)
        sampled_config[col] = column_config

    # Add the performance values to the sample

    search_results = add_performance(data, config_columns, performance_column, sampled_config, worst_value)

    # Convert search results to a sorted dataframe (ascending for minimisation)
    search_results = pd.DataFrame(search_results, columns=data.columns).sort_values(by=performance_column, ascending=not maximization)

    # Assign a distribution to the initial sample and use this to generate a new sample
    search_config = pd.DataFrame()
    distribution = [0.6, 0.25, 0.1, 0.05]
    distribution = np.repeat(distribution, SAMPLE_BUDGET/len(distribution))/int(SAMPLE_BUDGET/len(distribution))
    distribution = np.pad(distribution, (0, int(SAMPLE_BUDGET) % len(distribution)), 'constant')
    for col in config_columns:
        search_config[col] = random.shuffle(np.random.choice(search_results[col], int(REMAINING_BUDGET), p=distribution))

    # Get performance values
    search_results_2 = add_performance(data, config_columns, performance_column, search_config, worst_value)
    search_results_2 = pd.DataFrame(search_results_2, columns=data.columns).sort_values(by=performance_column, ascending=not maximization)
    
    #print(search_results)
    #print(search_results_2)
    
    # Export results to csv (combine search_results and search_results_2)
    results = pd.concat([search_results, search_results_2]).sort_values(by=performance_column, ascending=not maximization)
    results.to_csv(output_file, index=False)

    # Get best solution
    if maximization:
        best_solution = results.iloc[0].to_numpy()
    if not maximization:
        best_solution = results.iloc[0].to_numpy()

    # Get best performance score
    best_performance = best_solution[-1]

    return [int(x) for x in best_solution], best_performance


# This method gets the performance values from the dataset and appends it to the given samples 
def add_performance(data, config_columns, performance_column, sampled_config, worst_value):
    search_results = []
    for index, sample in sampled_config.iterrows():
        # Create a Pandas Series from the sampled configuration and match it against all rows in the dataset
        # The .all(axis=1) ensures that the match is applied across all configuration columns
        matched_row = data.loc[(data[config_columns] == sample).all(axis=1)]

        # if exists, add performance to performance column
        if not matched_row.empty:
            performance = matched_row[performance_column].iloc[0]
            sample = np.append(sample.to_numpy(), [performance])
        # if doesn't exist, give it the worst performance
        else:
            performance = worst_value
            sample = np.append(sample.to_numpy(), [performance])

        search_results.append(sample)
    return search_results