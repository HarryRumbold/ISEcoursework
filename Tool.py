import pandas as pd
import numpy as np
import os
import random
import matplotlib.pyplot as plt
import math

# Remove scientific notation e.g. 3.487e+03, easier for testing
np.set_printoptions(suppress=True)

#
# Hyperparameters
#
# Percentage used in step 1
SAMPLE_BUDGET = 0.5
# Percentage of configurations kept for step 2
SEARCH_BUDGET = 0.1
# Remaining budget to be used in step 2
REMAINING_BUDGET = 1 - SAMPLE_BUDGET

def search(file_path, budget, output_file):
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

    # Store all search results
    search_results = []


    #
    # Actually search
    #

    # Create first samples, sampled_config is a batch of configurations
    sampled_config = pd.DataFrame()
    for col in config_columns:
        # start with a uniformly random spread using 50% of the budget
        column_config = np.random.choice(data[col].unique(), int(budget * SAMPLE_BUDGET))
        random.shuffle(column_config)
        sampled_config[col] = column_config

    # For each configuration, check it exists in the dataset
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


    # Select top 10% of performers
    # Convert search results to a sorted dataframe (ascending for minimisation)
    search_results = pd.DataFrame(search_results, columns=data.columns).sort_values(by=['performance'], ascending=not maximization).head(math.floor(len(search_results) * SEARCH_BUDGET))
    print(search_results)
    # Collect distribution, and create new configurations using np.random.choice(p=[?, ?, ?, ?]) (this creates randomly with the same distribution as top performers)
    # Creates new columns one-by-one to be stitched together
    search_config = pd.DataFrame()
    for col in config_columns:
        distribution = []
        for val in sorted(search_results[col].unique()):
            distribution.append(search_results[col].value_counts().get(val, 0) / len(search_results))
        # Creates a new column with values matching the same distribution as the first sample
        column_new = np.random.choice(sorted(search_results[col].unique()), int(budget * REMAINING_BUDGET), p=distribution)
        #print(column_new)
        search_config[col] = column_new
    
    print(search_config)

    # get performance values

    # evaluate results

    return 0