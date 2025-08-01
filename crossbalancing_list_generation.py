import itertools
import pandas as pd

# Define the experimental design
# Each key is a factor, and the value is a tuple: (list of levels, 'within' or 'between')
factors = {
    "Color Layout": (["BGR", "RGB", "GBR"], "within"),
    "Empty Box Location": (["left", "right"], "within"),
    "Trial Type": (["impossible", "guess", "correct-inference"], "between")
}

# Separate within- and between-subject factors
within_factors = {k: v[0] for k, v in factors.items() if v[1] == "within"}
between_factors = {k: v[0] for k, v in factors.items() if v[1] == "between"}

# Generate Cartesian product of within-subject factors
within_keys = list(within_factors.keys())
within_values = list(within_factors.values())
within_combinations = list(itertools.product(*within_values))

# Create a DataFrame for each between-subject condition
condition_rows = []
for between_combination in itertools.product(*between_factors.values()):
    between_dict = dict(zip(between_factors.keys(), between_combination))
    for combo in within_combinations:
        row = dict(zip(within_keys, combo))
        row.update(between_dict)
        condition_rows.append(row)

# Convert to DataFrame
conditions_df = pd.DataFrame(condition_rows)

conditions_df.to_csv("lists/trial-conditions.csv", index=False)