# https://github.com/ideas-labo/ISE-solution/tree/main/lab3
# https://github.com/ideas-labo/ISE/tree/main/lab3

import pandas as pd
import numpy as np
import os


# Define the random search function
def random_search(file_path, budget, output_file):
    # Load the dataset
    data = pd.read_csv(file_path)

    # Identify the columns for configurations and performance
    config_columns = data.columns[:-1]
    performance_column = data.columns[-1]

    # Determine if this is a maximization or minimization problem
    # maximize throughput and minimize runtime
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

    for _ in range(budget):
        # Randomly sample a configuration
        # For each configuration column, randomly select a value from the unique values available in the dataset
        # This ensures that the sampled configuration is within the valid domain of each parameter
        sampled_config = [int(np.random.choice(data[col].unique())) for col in config_columns]

        # Check if the configuration exists in the dataset
        # Create a Pandas Series from the sampled configuration and match it against all rows in the dataset
        # The .all(axis=1) ensures that the match is applied across all configuration columns
        matched_row = data.loc[(data[config_columns] == pd.Series(sampled_config, index=config_columns)).all(axis=1)]

        if not matched_row.empty:
            # Existing configuration
            performance = matched_row[performance_column].iloc[0]
        else:
            # Non-existing configuration
            performance = worst_value

        # Update the best solution
        if maximization:
            if performance > best_performance:
                best_performance = performance
                best_solution = sampled_config
        else:
            if performance < best_performance:
                best_performance = performance
                best_solution = sampled_config

        # Record the current search result
        search_results.append(sampled_config + [performance])

    # Save the search results to a CSV file
    columns = list(config_columns) + ["Performance"]
    search_df = pd.DataFrame(search_results, columns=columns).sort_values(by="Performance", ascending=not maximization)
    search_df.to_csv(output_file, index=False)

    return [int(x) for x in best_solution], best_performance